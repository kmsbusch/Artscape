import photomosaic as pm
import numpy as np
from tqdm import tqdm
from skimage import img_as_float

def modifiedBasicMosaic(image, pool, grid_dims, mask=None, depth=0):
    image = img_as_float(image)
    image = pm.rescale_commensurate(image, grid_dims, depth)
    if mask is not None:
        mask = pm.rescale_commensurate(mask)

    # Use perceptually uniform colorspace for all analysis.
    converted_img = pm.perceptual(image)

    # Adapt the color palette of the image to resemble the palette of the pool.

    #adapted_img = pm.adapt_to_pool(converted_img, pool)


    # Partition the image into tiles and characterize each one's color.


    #converted_img was adapted_img, recomment line 49 back in
    tiles = pm.partition(converted_img, grid_dims=grid_dims, mask=mask, depth=depth)
    tile_colors = [np.mean(converted_img[tile].reshape(-1, 3), 0)
                  for tile in tqdm(tiles, desc='analyzing tiles')]

    # Match a pool image to each tile.
    match = pm.simple_matcher(pool)
    matches = [match(tc) for tc in tqdm(tile_colors, desc='matching')]

    # Draw the mosaic.
    canvas = np.ones_like(image)  # white canvas same shape as input image
    mosaic = pm.draw_mosaic(canvas, tiles, matches)
    finalMosaic = '/home/kmsbusch/mysite/images/madeMosaic.png'
    pm.imsave(finalMosaic,mosaic)


    fname = finalMosaic.rsplit('/',1)[1]

    returnMosaic = '/static/' + fname
    return returnMosaic, matches
