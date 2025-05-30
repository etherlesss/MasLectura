from sklearn.decomposition import TruncatedSVD

'''
    Embedding: Representación vectorial. De usuarios y libros en este caso.
    n_components: Número de dimensiones del embedding.
    random_state: Semilla para la aleatoriedad, para reproducibilidad.
'''

# Entrenar un modelo SVD con la matriz de utilidad centrada.
def trainSVD(centeredMatrix, n_components):
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    userEmbeddings = svd.fit_transform(centeredMatrix)
    bookEmbeddings = svd.components_.T # libros x componentes

    # print("Embeddings de usuarios")
    # print(userEmbeddings[:5])  # Mostrar los primeros 5 usuarios
    # print("Embeddings de libros")
    # print(bookEmbeddings[:5])  # Mostrar los primeros 5 libros
    
    return svd, userEmbeddings, bookEmbeddings