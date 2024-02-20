from skimage import img_as_float
import photomosaic as pm
import matplotlib.pyplot as plt
import numpy
#image = img_as_float("C:/Users/Kevin Busch/Documents/CSCI3308/Artscape/testimage1.jpg")
def makeMosaic(fileName):
    nameIn = fileName.rsplit('/',1)[1]
    image = pm.imread('/home/kmsbusch/mysite/images/pool/newPool/' + nameIn)

    #pool = pm.make_pool("/home/kmsbusch/mysite/images/pool/newPool/*.jpg")
    #pm.export_pool(pool, '/home/kmsbusch/mysite/images/pool/image_pool.pool')
    pool = pm.import_pool('/home/kmsbusch/mysite/images/pool/image_pool.pool')



    converted_img = pm.perceptual(image)

    #contrasted some weird way from website
    #pm.plot_palette(pm.color_palette(list(pool.values())))
    #djusted_img = pm.adapt_to_pool(converted_img, pool)
    #pm.plot_palette(pm.color_palette(adjusted_img))
    #scaled_img = pm.rescale_commensurate(adjusted_img, grid_dims=(50, 50), depth=0)

    #original method
    pm.plot_palette(pm.color_palette(converted_img))
    adapted_img = pm.adapt_to_pool(converted_img, pool)
    scaled_img = pm.rescale_commensurate(adapted_img, grid_dims=(50, 50), depth=0)

    tiles = pm.partition(scaled_img, grid_dims=(50, 50), depth=0)



    # Reshape the 3D array (height, width, color_channels) into
    # a 2D array (num_pixels, color_channels) and average over the pixels.
    #uncomment
    tile_colors = [numpy.mean(scaled_img[tile].reshape(-1, 3), 0) for tile in tiles]

    # Match a pool image to each tile.
    #uncomment
    match = pm.simple_matcher(pool)
    matches = [match(tc) for tc in tile_colors]

    #uncomment
    #canvas = numpy.ones_like(scaled_img)  # white canvas
    # canvas = numpy.zeros_like(scaled_img)  # black canvas


    mosaic = pm.basic_mosaic(image,pool,(50,50)) # make 200*200 mosaic


    finalMosaic = '/home/kmsbusch/mysite/images/madeMosaic.jpg'
    # Draw the mosaic.
    #mos = pm.draw_mosaic(canvas, tiles, matches)


    #pm.imsave(finalMosaic,mos)
    pm.imsave(finalMosaic,mosaic)
    # cache = {}
    # mos1 = pm.draw_mosaic(canvas1, tiles1, matches1, resized_copy_cache=cache)
    # # Now cache is filled with resized copies of any images used in ``mos1``.

    # # This will be faster:
    # mos2 = pm.draw_mosaic(canvas2, tiles2, matches2, resized_copy_cache=cache)
    fname = finalMosaic.rsplit('/',1)[1]

    returnMosaic = '/static/' + fname


    return returnMosaic, matches



