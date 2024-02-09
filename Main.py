import math
import random

half_height, half_width = 1,1
object_array = []

def add_triangle(v1, v2, v3, colour):
    tri = [v1, v2, v3, colour]
    object_array.append(tri)

def random_colour():
    hexlen = 0
    while hexlen != 7:
        random_number = random.randint(0, 16777215)
        hex_number = '#' + format(random_number, 'x')
        hexlen = len(hex_number)
    return hex_number

def load_mtl(file_name):
    file = open(file_name, "rt")
    materials = []
    for line in file:
        if "# Material Count:" in line:
            num_materials = line.split[-1]
        if "newmtl" in line:
            current_material = line.split[-1]
    return materials

def get_normal_from_triangle(x1,y1,z1,x2,y2,z2,x3,y3,z3):
    lx1, ly1, lz1 = x2 - x1, y2 - y1, z2 - z1
    lx2, ly2, lz2 = x3 - x1, y3 - y1, z3 - z1
    nx,ny,nz = ly1 * lz2 - lz1 * ly2, lz1 * lx2 - lx1 * lz2, lx1 * ly2 - ly1 * lx2
    normal_length = math.sqrt(nx*nx+ny*ny+nz*nz)
    return nx/normal_length, ny/normal_length, nz/normal_length

def get_normal_from_angle(angle_x, angle_y, angle_z):
    x, y, z = 0,0,0
    x += math.cos(angle_z)
    y += math.sin(angle_z)
    x += math.cos(angle_x)
    z += math.sin(angle_x)
    z += math.cos(angle_y)
    y += math.sin(angle_y)
    return x,y,z

def get_dot_product(x1,y1,z1,x2,y2,z2):
    dp = x1*x2+y1*y2+z1*z2
    dpx, dpy, dpz = x1*x2, y1*y2, z1*z2
    l = math.sqrt(dpx*dpx+dpy*dpy+dpz*dpz)
    return dp/l

def render_wall_from_normalised_points(x1_3d,y1_3d,z1_3d,x2_3d,y2_3d,z2_3d,x3_3d,y3_3d,z3_3d,colour):
    global half_width, half_height
    nx,ny,nz = get_normal_from_triangle(x1_3d,y1_3d,z1_3d,x2_3d,y2_3d,z2_3d,x3_3d,y3_3d,z3_3d)
    #camera_nx, camera_ny, camera_nz = get_normal_from_angle(angle_x, angle_y, angle_z)
    #dp = get_dot_product(nx, ny, nz, camera_nx, camera_ny, camera_nz)
    if nz <=0:
        x1_2d = x1_3d*half_width+half_width
        y1_2d = y1_3d*half_height+half_height
        x2_2d = x2_3d*half_width+half_width
        y2_2d = y2_3d*half_height+half_height
        x3_2d = x3_3d*half_width+half_width
        y3_2d = y3_3d*half_height+half_height
        return [int(x1_2d),int(y1_2d),int(x2_2d),int(y2_2d),int(x3_2d),int(y3_2d),colour]

def rotate_point_z_axis(x,y,z, angle):
    rx = x * math.cos(angle) - y * math.sin(angle)
    ry = x * math.sin(angle) + y * math.cos(angle)
    rz = z
    return rx,ry,rz

def rotate_point_y_axis(x,y,z, angle):
    rx = x * math.cos(angle) - z * math.sin(angle)
    ry = y
    rz = x * math.sin(angle) + z * math.cos(angle)
    return rx,ry,rz

def rotate_point_x_axis(x,y,z, angle):
    rx = x
    ry = y * math.cos(angle) - z * math.sin(angle)
    rz = y * math.sin(angle) + z * math.cos(angle)
    return rx,ry,rz

def scale_point(x,y,z, zfar, znear, fov, ar, camera_x, camera_y, camera_z ,camera_angle_x, camera_angle_y, camera_angle_z):
    x,y,z = rotate_point_z_axis(x,y,z, camera_angle_z)
    x,y,z = rotate_point_y_axis(x,y,z, camera_angle_y)
    x,y,z = rotate_point_x_axis(x,y,z, camera_angle_x)
    x,y,z = camera_x+x,camera_y+y,camera_z+z
    if z != 0:
        x = (ar*(1/math.tan(fov/2))*x)/z
        y = ((1/math.tan(fov/2))*y)/z
        z = z*(zfar/(zfar-znear))-((zfar*znear)/(zfar-znear))
    return [x,y,z]



class object:
    def __init__(self, _model, x = 0, y = 0 , z = 0, ax = 0, ay = 0, az = 0, colour = None):
        ax, ay, az = math.radians(ax), math.radians(ay), math.radians(az)
        model = open(_model, 'rt')
        count = 0
        for line in model:
            if line[0] == 'v' and line[1] == ' ':
                count+=1
                split = line.split()
                while split[1][-1] == '0' or split[1][-1] == '.':
                    if split[1][-1] == '.':
                        split[1] = split[1][:-1]
                        break
                    else:
                        split[1] = split[1][:-1]
                while split[2][-1] == '0' or split[2][-1] == '.':
                    if split[2][-1] == '.':
                        split[2] = split[2][:-1]
                        break
                    else:
                        split[2] = split[2][:-1]
                while split[3][-1] == '0' or split[3][-1] == '.':
                    if split[3][-1] == '.':
                        split[3] = split[3][:-1]
                        break
                    else:
                        split[3] = split[3][:-1]
                split[1], split[2], split[3] = rotate_point_z_axis(float(split[1]), float(split[2]), float(split[3]), az)
                split[1], split[2], split[3] = rotate_point_y_axis(float(split[1]), float(split[2]), float(split[3]), ay)
                split[1], split[2], split[3] = rotate_point_x_axis(float(split[1]), float(split[2]), float(split[3]), ax)
                locals()["v"+str(count)] = [float(split[1]) + x, float(split[2]) - y, float(split[3]) + z]
            elif line[0] == 'f' and line[1] == ' ':
                split = line.split()
                for i in range(0, len(split)):
                    pos = 0
                    v, vt, vn = '', '', ''
                    for q in range(0, len(split[i])):
                        if i != 0:
                            char = split[i][q]
                            if char == '/':
                                pos += 1
                            else:
                                if pos == 0:
                                    v += char
                                elif pos == 1:
                                    vt += char
                                elif pos == 2:
                                    vn += char
                    if i != 0:
                        locals()["fv" + str(i)] = locals()["v"+str(v)]
                if colour == None:
                    new_colour = random_colour()
                else:
                    new_colour = colour
                for p in range(2,len(split)-1):
                    add_triangle(locals()["fv1"], locals()["fv"+str(p)], locals()["fv"+str(p+1)], new_colour)

    def get_object(self):
        global object_array
        return object_array

class gl:
    map_array = []    
    def __init__(self, _width = 1920, _height = 1080, _fov = math.radians(55), _zfar = 1000, _znear = 0.1):
        global half_width, half_height
        self.camera_x, self.camera_y, self.camera_z = 0,0,0
        self.camera_angle_x, self.camera_angle_y, self.camera_angle_z = 0,0,0
        self.ar = int(_height)/int(_width)
        half_width, half_height = int(_width/2), int(_height/2)
        self.zfar, self.znear, self.fov = _zfar, _znear, _fov
        self.width = _width
        self.height = _height

    def camera_absolute(self, _camera_x = None, _camera_y = None, _camera_z = None, _camera_angle_x = None, _camera_angle_y = None, _camera_angle_z = None):
        if _camera_x != None:
            self.camera_x = _camera_x
        if _camera_y != None:
            self.camera_y = _camera_y
        if _camera_z != None:
            self.camera_z = _camera_z
        if _camera_angle_x != None:
            self.camera_angle_x = math.radians(_camera_angle_x)
        if _camera_angle_y != None:
            self.camera_angle_y = math.radians(_camera_angle_y)
        if _camera_angle_z != None:
            self.camera_angle_z = math.radians(_camera_angle_z)

    def move_camera(self, _camera_x = 0, _camera_y = 0, _camera_z = 0, _camera_angle_x = 0, _camera_angle_y = 0, _camera_angle_z = 0):
        self.camera_z += math.cos(self.camera_angle_y) * _camera_z
        self.camera_x += math.sin(self.camera_angle_y) * _camera_z
        
        self.camera_x += math.sin(self.camera_angle_y+math.pi/2) * _camera_x
        self.camera_z += math.cos(self.camera_angle_y+math.pi/2) * _camera_x
        
        self.camera_y = self.camera_y + _camera_y
        
        self.camera_angle_x, self.camera_angle_y, self.camera_angle_z = self.camera_angle_x + math.radians(_camera_angle_x), self.camera_angle_y + math.radians(_camera_angle_y), self.camera_angle_z + math.radians(_camera_angle_z)

    def new_frame(self):
        frame = []
        for model in self.map_array:
            for wall_num in range(0,len(model)):
                wall = model[wall_num]
                for point in range(0,len(wall)-1):
                    locals()["sp" + str(point) + str(wall_num)] = scale_point(wall[point][0],wall[point][1],wall[point][2], self.zfar, self.znear, self.fov, self.ar, self.camera_x, self.camera_y, self.camera_z , self.camera_angle_x, self.camera_angle_y, self.camera_angle_z)
                temp_tri = render_wall_from_normalised_points(locals()["sp0"+ str(wall_num)][0],locals()["sp0"+ str(wall_num)][1],locals()["sp0"+ str(wall_num)][2],locals()["sp1"+ str(wall_num)][0],locals()["sp1"+ str(wall_num)][1],locals()["sp1"+ str(wall_num)][2],locals()["sp2"+ str(wall_num)][0],locals()["sp2"+ str(wall_num)][1],locals()["sp2"+ str(wall_num)][2],wall[len(wall)-1])
                if temp_tri != None:
                    frame.append(temp_tri)
        return frame
