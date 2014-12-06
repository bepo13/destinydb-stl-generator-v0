import numpy

scale = 1000

def unit(v):
    return (v / numpy.linalg.norm(v))

def angle(v1, v2):
    v1_u = unit(v1)
    v2_u = unit(v2)
    angle = numpy.arccos(numpy.dot(v1_u, v2_u))
    if numpy.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return numpy.pi
    return angle

def generate(models, solidName, fileName):
    # Find the minimum positional vector for all models
    positionMin = numpy.array([0, 0, 0, 0], dtype='float')
    for model in models:
        for geometry in model.geometry.geometry:
            for mesh in geometry.meshes.meshes:
                positions = mesh.positions
                for v in positions:
                    if v[0] < positionMin[0]:
                        positionMin[0] = v[0]
                    if v[1] < positionMin[1]:
                        positionMin[1] = v[1]
                    if v[2] < positionMin[2]:
                        positionMin[2] = v[2]
                    if v[3] < positionMin[3]:
                        positionMin[3] = v[3]
                        
    # Translate position coordinates to always be positive
    positionMin *= -1
    
    #Open file
    with open(fileName, 'w') as f:
        print("Writing "+fileName+"...")
                 
        # Write name header
        f.write("solid "+solidName+"\n")
        
        # Iterate through all models
        for model in models:
            # Write positional vectors (once to start)
            for geometry in model.geometry.geometry:
                for mesh in geometry.meshes.meshes:
                    indices = mesh.indices.data
                    positions = mesh.positions
                    normals = mesh.normals
                    parts = mesh.parts.data
                    
                    # Loop through all the parts in the mesh
                    for i, part in enumerate(parts):                    
                        # Check if this part has been duplicated
                        ignore = False
                        for j in range(i):
                            if (parts[i].indexStart == parts[j].indexStart) or (parts[i].indexCount == parts[j].indexCount):
                                ignore = True
                                
                        # Skip anything meeting one of the following::
                        #   duplicate part
                        #   levelOfDetail greater than one
                        #   diffuseTexture.contains("target_reticles")
                        if ignore or part.levelOfDetail > 1 or ("target_reticles" in part.diffuseTexture):
                            continue
                        
                        start = part.indexStart
                        count = part.indexCount
                        
                        # Process indices in sets of 3
                        if part.primitive == 3:
                            increment = 3
                        # Process indices as triangle strip
                        elif part.primitive == 5:
                            increment = 1
                            count -= 2
                            
                        j = 0
                        while j < count:
                            # Skip if any two of the indices match (ignoring lines)
                            if (indices[start+j+0] == indices[start+j+1]) or (indices[start+j+0] == indices[start+j+2]) or (indices[start+j+1] == indices[start+j+2]):
                                j += 1
                                continue
                                
                            # Calculate the average normal
                            n = (normals[indices[start+j+0]] + normals[indices[start+j+1]] + normals[indices[start+j+2]])[0:3]
                            
                            # Calculate normal of vertices
                            v1 = positions[indices[start+j+1]][0:3] - positions[indices[start+j+0]][0:3]
                            v2 = positions[indices[start+j+2]][0:3] - positions[indices[start+j+1]][0:3]
                            n2 = numpy.cross(v1, v2)
                            
                            # Calculate the angle between the two normals
                            # Reverse the vertices orientation if the angle is > pi/2 (90*)
                            a = angle(unit(n), unit(n2))
                            if a > numpy.pi/2:
                                flip = True
                            else:
                                flip = False
                                
                            # Write the normal and loop start to file
                            # the normal doesn't matter for this, the order of vertices does
                            f.write("facet normal 0.0 0.0 0.0\n")
                            f.write("  outer loop\n")
                            
                            if flip:
                                # write the three vertices to the file in reverse order
                                k = 3
                                while k > 0:
                                    v = positions[indices[start+j+(k-1)]]
                                    v = (v + positionMin) * scale
                                    f.write("    vertex "+str(v[0])+" "+str(v[1])+" "+str(v[2])+"\n")
                                    k -= 1
                            else:
                                # write the three vertices to the file in forward order
                                for k in range(3):
                                    v = positions[indices[start+j+k]]
                                    v = (v + positionMin) * scale
                                    f.write("    vertex "+str(v[0])+" "+str(v[1])+" "+str(v[2])+"\n")
                            
                            # Write the loop and normal end to file
                            f.write("  endloop\n")
                            f.write("endfacet\n")
                            
                            j += increment
                        else:
                            # Skip this if it ever happens
                            continue
        f.close()
    
    return