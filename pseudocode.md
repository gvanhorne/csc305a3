    # for c in range(width):
    #   for r in range(height):
    #     print(f"Pixel Coordinate: ({c}, {r})")

    # Function Main
      # for each pixel (c,r) on screen
      #  determine ray rc,r from eye through pixel
      #  ray.setDepth(1)
      #  colour(c,r) = raytrace(rc,r )
      # end for
    # end
    # function raytrace(r)
      # if (ray.depth() > MAX_DEPTH) return black
      # P = closest intersection of ray with all objects
      # if( no intersection ) return backgroundcolour
      # clocal = Sum(shadowRays(P,Lighti))
      # cre = raytrace(rre)
      # return (clocal+kre*cre)
    # end
