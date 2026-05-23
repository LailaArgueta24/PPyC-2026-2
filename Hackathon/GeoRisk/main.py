import rasterio
import numpy as np
import matplotlib.pyplot as plt

ruta_imagen = './input/Forest_1.tiff'
#ruta_imagen = './input/Industrial_10.tiff'

with rasterio.open(ruta_imagen) as dataset:
    # Rasterio lee las bandas con índices del 1 al 13 (no desde 0)
    
    # Extraer las bandas visibles (RGB)
    banda_roja = dataset.read(4)   # Banda 4 = Rojo
    banda_verde = dataset.read(3)  # Banda 3 = Verde
    banda_azul = dataset.read(2)   # Banda 2 = Azul
    
    # Extraer una banda invisible al ojo humano
    banda_nir = dataset.read(8)    # Banda 8 = Infrarrojo Cercano (Near-Infrared)

rgb = np.dstack([banda_roja, banda_verde, banda_azul]).astype(float)
rgb /= np.max(rgb) if np.max(rgb) != 0 else 1.0

# El NDVI se calcula como: (NIR - Red) / (NIR + Red)
denominador = banda_nir.astype(float) + banda_roja.astype(float)
ndvi = np.where(denominador == 0, 0, (banda_nir.astype(float) - banda_roja.astype(float)) / denominador)


# El EVI se calcula como: 2.5 * (NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1)
denominador_evi = banda_nir.astype(float) + 6 * banda_roja
denominador_evi -= 7.5 * banda_azul.astype(float) + 1
evi = np.where(denominador_evi == 0, 0, 2.5 * (banda_nir.astype(float) - banda_roja.astype(float)) / denominador_evi)

# Sequía extrema (caída abrupta del NDVI/EVI)

indicadorSequia = ndvi / evi


fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].imshow(rgb)
axes[0].set_title('Imagen RGB original')
axes[0].axis('off')

ndvi_plot = axes[1].imshow(ndvi, cmap='RdYlGn')
axes[1].set_title('Indice de Vegetacion (NDVI)')
axes[1].axis('off')
fig.colorbar(ndvi_plot, ax=axes[1], fraction=0.046, pad=0.04, label='NDVI')


# ndvi_plot2 = axes[1].imshow(indicadorSequia, cmap='RdYlGn')
# axes[1].set_title('Indice de Sequía (NDVI/EVI)')
# axes[1].axis('off')
# fig.colorbar(ndvi_plot2, ax=axes[1], fraction=0.046, pad=0.04, label='NDVI/EVI')

plt.tight_layout()
plt.show()
