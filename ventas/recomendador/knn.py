
from ventas.models import CatalogProduct, Product
from ventas.recomendador.api_facebook import get_data_facebook
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

from ventas.serializers import CatalogProductSerializer


def run_knn(id_producto):
    #Obtiene datos de facebook, con sus comentarios
    data = get_data_facebook()
    #procesa a solo comentarios.
    process_data = data.get("published_posts").get("data")
    data_for_knn = []
    for dat in process_data:
        if dat.get("comments"):
            comments = []
            for mess in dat.get("comments").get("data"):
                comments.append(mess.get("message"))
            data_for_knn.append({"id":dat.get("id"),"messages":comments})
            
        print(f"dat {dat}")
    df = pd.DataFrame(data_for_knn)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([" ".join(comentarios) for comentarios in df['messages']])
    knn_model = NearestNeighbors(n_neighbors=3, metric='cosine')
    knn_model.fit(tfidf_matrix)

    def hacer_recomendacion(producto, n_recomendaciones=1):
       # print(f"length producto {len(df[df['id'] == producto])}")
        #print(f"df {(df[df['id'] == producto])}")
        if len(df[df['id'] == producto])<=0:
            return []
        else:
            idx = df[df['id'] == producto].index[0]
            distancia, indice = knn_model.kneighbors(tfidf_matrix[idx], n_neighbors=n_recomendaciones+1)
            # Excluimos el primer elemento, ya que es el mismo producto (distancia cero)
            indice_recomendaciones = indice[0][1:]
            recomendaciones = df.iloc[indice_recomendaciones]['id'].tolist()
            return recomendaciones

    #producto = '116784698104891_143228125467843'
    producto = Product.objects.get(id=id_producto)
    #print(f"producto.id_publisher {producto.id_publisher}")
    recomendaciones_producto1 = hacer_recomendacion(producto.id_publisher)
    #print(f"recomendaciones_producto1 {recomendaciones_producto1}")
    list_products = []
    for producto_label in recomendaciones_producto1:
        #print(f"producto_label {producto_label}")
        dat = None
        try:
            dat = Product.objects.get(id_publisher=producto_label)
        
            #list_catalog = []
            #for catalog in CatalogProduct.objects.filter(product=dat):
            #    print(f"catalog {catalog}")            
            #    list_catalog.append(catalog)
            #print(f"catalog {list_catalog}")
        
            if dat!=None:
                list_products.append(dat)
        except Product.DoesNotExist:
            pass
    #return recomendaciones_producto1
    return list_products