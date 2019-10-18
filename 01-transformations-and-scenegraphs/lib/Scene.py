#!/usr/bin/python3

# import avango-guacamole libraries
import avango
import avango.gua

# import python libraries
import math
import time

# appends the objects to the scenegraph that will be visualized
class Scene:

    def __init__(self, scenegraph):
        self.scenegraph = scenegraph
        self.loader = avango.gua.nodes.TriMeshLoader()

        # build scene light and grid floor
        self.build_light()
        self.build_floor()

        # build monkey task
        self.num_monkey_tasks = 8
        self.load_wireframe_task_monkeys()

        # transformation matrices for monkey task solution using the avango.gua module
        transformation_matrices = []   
        
        # YOUR CODE - BEGIN (Exercise 1.1 - Transformation Matrices)
        transformation_matrices.append(avango.gua.make_trans_mat(-4.0, 1.0, -1.0)*avango.gua.make_rot_mat(30, 0, 1, 0))
        transformation_matrices.append(avango.gua.make_trans_mat(-3.0, 1.0, -1.0)*avango.gua.make_rot_mat(40, 1, 0, 0))
        transformation_matrices.append(avango.gua.make_trans_mat(-2.0, 2.0, 2.0)*avango.gua.make_rot_mat(120, 0, 1, 0)*avango.gua.make_rot_mat(-20, 1, 0, 0))
        transformation_matrices.append(avango.gua.make_trans_mat(-2.0, 1.0, 0.0)*avango.gua.make_scale_mat(2, 2, 2)*avango.gua.make_rot_mat(-120, 0, 0, 1))
        transformation_matrices.append(avango.gua.make_trans_mat(0.0, 3.0, 0.0)*avango.gua.make_rot_mat(100, 0, 1, 0)*avango.gua.make_rot_mat(0, 0, 0, 1)*avango.gua.make_rot_mat(40, 1, 0, 0))#*avango.gua.make_rot_mat(100, 0, 1, 0)*avango.gua.make_rot_mat(40, 1, 0, 0)*avango.gua.make_rot_mat(10, 0, 0, 1))
        transformation_matrices.append(avango.gua.make_trans_mat(0.0, 0.5, 3.0)*avango.gua.make_scale_mat(1.5, 1.5, 1.5)*avango.gua.make_rot_mat(-100, 0, 1, 0)*avango.gua.make_rot_mat(-220, 1, 0, 0))
        transformation_matrices.append(avango.gua.make_trans_mat(2.0, 1.5, -2.0)*avango.gua.make_scale_mat(1.5, 1, 1))
        transformation_matrices.append(avango.gua.make_trans_mat(4.0, 1.0, 2.0)*avango.gua.make_scale_mat(2, 2, 2))
        # YOUR CODE - END (Exercises 1.1 - Transformation Matrices)

        # transformation matrices for monkey task solution using own matrix creation functions
        own_transformation_matrices = []

        # YOUR CODE - BEGIN (Exercise 1.2 - Verfication)
        own_transformation_matrices.append(self.make_trans_mat(-4.0, 1.0, -1.0)*self.make_rot_mat(30, 0, 1, 0))
        own_transformation_matrices.append(self.make_trans_mat(-3.0, 1.0, -1.0)*self.make_rot_mat(40, 1, 0, 0))
        own_transformation_matrices.append(self.make_trans_mat(-2.0, 2.0, 2.0)*self.make_rot_mat(120, 0, 1, 0)*self.make_rot_mat(-20, 1, 0, 0))
        own_transformation_matrices.append(self.make_trans_mat(-2.0, 1.0, 0.0)*self.make_scale_mat(2, 2, 2)*self.make_rot_mat(-120, 0, 0, 1))
        own_transformation_matrices.append(self.make_trans_mat(0.0, 3.0, 0.0)*self.make_rot_mat(100, 0, 1, 0)*self.make_rot_mat(0, 0, 0, 1)*self.make_rot_mat(40, 1, 0, 0))
        own_transformation_matrices.append(self.make_trans_mat(0.0, 0.5, 3.0)*self.make_scale_mat(1.5, 1.5, 1.5)*self.make_rot_mat(-100, 0, 1, 0)*self.make_rot_mat(-220, 1, 0, 0))
        own_transformation_matrices.append(self.make_trans_mat(2.0, 1.5, -2.0)*self.make_scale_mat(1.5, 1, 1))
        own_transformation_matrices.append(self.make_trans_mat(4.0, 1.0, 2.0)*self.make_scale_mat(2, 2, 2))
        # YOUR CODE - BEGIN (Exercise 1.2 - Verification)

        # transformation matrices for monkey task solution using own matrix multiplication
        own_multiplications = []

        # YOUR CODE - BEGIN (Exercise 1.3 - Verfication)
        own_multiplications.append(self.mult_mat(self.make_trans_mat(-4.0, 1.0, -1.0), self.make_rot_mat(30, 0, 1, 0)))#self.make_trans_mat(-4.0, 0.0, 0.0), self.make_trans_mat(0.0, 0.0, 0.0)))
        own_multiplications.append(self.mult_mat(self.make_trans_mat(-3.0, 0.0, 0.0), self.make_trans_mat(0.0, 0.0, 0.0)))
        own_multiplications.append(self.mult_mat(self.make_trans_mat(-2.0, 0.0, 0.0), self.make_trans_mat(0.0, 0.0, 0.0)))
        own_multiplications.append(self.mult_mat(self.make_trans_mat(-1.0, 0.0, 0.0), self.make_trans_mat(0.0, 0.0, 0.0)))
        own_multiplications.append(self.mult_mat(self.make_trans_mat(1.0, 0.0, 0.0), self.make_trans_mat(0.0, 0.0, 0.0)))
        own_multiplications.append(self.mult_mat(self.make_trans_mat(2.0, 0.0, 0.0), self.make_trans_mat(0.0, 0.0, 0.0)))
        own_multiplications.append(self.mult_mat(self.make_trans_mat(3.0, 0.0, 0.0), self.make_trans_mat(0.0, 0.0, 0.0)))
        own_multiplications.append(self.mult_mat(self.make_trans_mat(4.0, 0.0, 0.0), self.make_trans_mat(0.0, 0.0, 0.0)))
        # YOUR CODE - BEGIN (Exercise 1.3 - Verfication)

        # YOUR CODE - BEGIN (Toggle between matrices to be applied to monkeys)
        #self.load_solid_solution_monkeys(transformation_matrices)
        #self.load_solid_solution_monkeys(own_transformation_matrices)
        self.load_solid_solution_monkeys(own_multiplications)
        # YOUR CODE - END (Toggle between matrices to be applied to monkeys)

        # YOUR CODE - BEGIN (Uncomment before starting with Exercise 1.4)
        #self.build_equal_rotation_task()
        # YOUR CODE - END (Uncomment before starting with Exercise 1.4)

        # YOUR CODE - BEGIN (Uncomment before starting with Exercise 1.5)
        #self.build_rotating_monkeys()
        # YOUR CODE - END (Uncomment before starting with Exercise 1.5)

        # YOUR CODE - BEGIN (Uncomment before starting with Exercise 1.8)
        #wt_computer = WorldTransformComputer()
        #wt_computer.sf_node.value = self.another_big_monkey
        # YOUR CODE - END (Uncomment before starting with Exercise 1.8)

    # adds a light to the scenegraph's root node
    def build_light(self):
        self.lamp_node = avango.gua.nodes.LightNode(Type=avango.gua.LightType.SPOT,
                                                    Name='lamp',
                                                    EnableShadows=True)
        self.lamp_node.Transform.value = avango.gua.make_trans_mat(0, 30, 0) * \
            avango.gua.make_rot_mat(-90, 1, 0, 0) * \
            avango.gua.make_scale_mat(550, 550, 300)
        self.scenegraph.Root.value.Children.value.append(self.lamp_node)

    # adds a grid floor and a coordinate system visualization to the scenegraph's root node
    def build_floor(self):
        self.ground_grid = self.loader.create_geometry_from_file('ground_grid',
                                                                 'data/objects/grid.obj',
                                                                 avango.gua.LoaderFlags.DEFAULTS)
        self.ground_grid.Material.value.set_uniform('Emissivity', 0.25)
        self.ground_grid.Material.value.set_uniform('Roughness', 0.8)
        self.ground_grid.Material.value.set_uniform(
            'Color', avango.gua.Vec4(0.4, 0.4, 0.4, 1.0))
        self.ground_grid.Material.value.EnableBackfaceCulling.value = False
        self.scenegraph.Root.value.Children.value.append(self.ground_grid)

        self.coordinate_system = self.loader.create_geometry_from_file('coordinate_system',
                                                                       'data/objects/coordinate_system.obj',
                                                                       avango.gua.LoaderFlags.LOAD_MATERIALS)
        self.apply_material_uniform_recursively(
            self.coordinate_system, 'Emissivity', 0.25)
        self.apply_material_uniform_recursively(
            self.coordinate_system, 'Roughness', 0.8)
        self.scenegraph.Root.value.Children.value.append(
            self.coordinate_system)

    # applys a material uniform to all TriMeshNode instances below the specified start node
    def apply_material_uniform_recursively(self, start_node, uniform_name, uniform_value):
        if start_node.__class__.__name__ == "TriMeshNode":
            start_node.Material.value.set_uniform(uniform_name, uniform_value)

        for child in start_node.Children.value:
            self.apply_material_uniform_recursively(
                child, uniform_name, uniform_value)

    # loads the wireframe monkeys with their secret transformations to be found in this assignment
    def load_wireframe_task_monkeys(self):
        self.wireframe_monkeys = []
        for i in range(1, self.num_monkey_tasks+1):
            wireframe_monkey = self.loader.create_geometry_from_file('wireframe_monkey_' + str(i),
                                                                     'data/objects/wireframe_monkey_task_' +
                                                                     str(i) +
                                                                     '.obj',
                                                                     avango.gua.LoaderFlags.DEFAULTS)
            wireframe_monkey.Material.value.set_uniform('Emissivity', 0.25)
            wireframe_monkey.Material.value.set_uniform('Roughness', 0.8)
            wireframe_monkey.Material.value.set_uniform(
                'Color', avango.gua.Vec4(1.0, 1.0, 1.0, 1.0))
            wireframe_monkey.Material.value.EnableBackfaceCulling.value = False
            self.wireframe_monkeys.append(wireframe_monkey)
            self.scenegraph.Root.value.Children.value.append(wireframe_monkey)

    # loads the solid monkeys indicating the transformation matrices specified by you
    # when the task was completed successfully, these monkeys align with the wireframe monkeys created above
    def load_solid_solution_monkeys(self, transformation_matrices):
        if len(transformation_matrices) != self.num_monkey_tasks:
            raise ValueError(
                'Error: The number of entries in transformation_matrices must match self.num_monkey_tasks.')

        for i in range(1, self.num_monkey_tasks+1):
            monkey = self.loader.create_geometry_from_file('monkey_' + str(i),
                                                           'data/objects/monkey.obj',
                                                           avango.gua.LoaderFlags.DEFAULTS)
            monkey.Transform.value = transformation_matrices[i-1]
            mat = avango.gua.nodes.Material()
            mat.set_uniform('Emissivity', 0.25)
            mat.set_uniform('Roughness', 0.8)
            red = ((i * 425) % 255) / 255.0
            green = ((i * 525) % 255) / 255.0
            blue = ((i * 640) % 255) / 255.0
            mat.set_uniform(
                'Color', avango.gua.Vec4(red, green, blue, 1.0))
            mat.EnableBackfaceCulling.value = False
            monkey.Material.value = mat
            self.scenegraph.Root.value.Children.value.append(monkey)

    # creates a translation matrix
    def make_trans_mat(self, tx, ty, tz):
        mat = avango.gua.Mat4()
        # YOUR CODE - BEGIN (Exercise 1.2 - Translation Matrices)
        mat.set_element(0,3,tx)
        mat.set_element(1,3,ty)
        mat.set_element(2,3,tz)
        #print(mat)
        # YOUR CODE - END (Exercise 1.2 - Translation Matrices)
        return mat

    # creates a rotation matrix
    def make_rot_mat(self, degrees, ax_x, ax_y, ax_z):
        mat = avango.gua.Mat4()
        # YOUR CODE - BEGIN (Exercise 1.2 - Rotation Matrices)
        if (ax_x == 1) :
            mat.set_element(1,1,math.cos(math.radians(degrees)))
            mat.set_element(1,2,-math.sin(math.radians(degrees)))
            mat.set_element(2,1,math.sin(math.radians(degrees)))
            mat.set_element(2,2,math.cos(math.radians(degrees)))
        if (ax_y == 1) :
            mat.set_element(0,0,math.cos(math.radians(degrees)))
            mat.set_element(2,0,-math.sin(math.radians(degrees)))
            mat.set_element(0,2,math.sin(math.radians(degrees)))
            mat.set_element(2,2,math.cos(math.radians(degrees)))
        if (ax_z == 1) :
            mat.set_element(0,0,math.cos(math.radians(degrees)))
            mat.set_element(0,1,-math.sin(math.radians(degrees)))
            mat.set_element(1,0,math.sin(math.radians(degrees)))
            mat.set_element(1,1,math.cos(math.radians(degrees)))
        # YOUR CODE - END (Exercise 1.2 - Rotation Matrices)
        return mat

    # creates a scaling matrix
    def make_scale_mat(self, sx, sy, sz):
        mat = avango.gua.Mat4()
        # YOUR CODE - BEGIN (Exercise 1.2 - Scaling Matrices)
        mat.set_element(0,0,sx)
        mat.set_element(1,1,sy)
        mat.set_element(2,2,sz)
        # YOUR CODE - END (Exercise 1.2 - Scaling Matrices)
        return mat

    # multiplies two matrix instances
    def mult_mat(self, lhs, rhs):
        result = avango.gua.Mat4()
        print("lhs: ", lhs)
        print("rhs: ", rhs)
        # YOUR CODE - BEGIN (Exercise 1.3 - Matrix Multiplication)
        for row in range(0,4):
            for col in range(0,4):
                s = 0
                for k in range(0,4):
                    s += lhs.get_element(row,k) * rhs.get_element(k,col)
                result.set_element(row,col,s)
        # YOUR CODE - END (Exercise 1.3 - Matrix Multiplication)
        print("result: ", result)
        return result

    # builds two coordinate systems that should have the same transformations
    # achieved by multiplying different matrices
    def build_equal_rotation_task(self):
        # YOUR CODE - BEGIN (Exercise 1.4 - Equal Rotations)
        alpha = 0
        beta = 90
        # YOUR CODE - END (Exercise 1.4 - Equal Rotations)

        mat1 = avango.gua.make_trans_mat(0.0, 4.0, 0.0) * \
               avango.gua.make_rot_mat(90, 1, 0, 0) * \
               avango.gua.make_rot_mat(alpha, 0, 0, 1)
        mat2 = avango.gua.make_trans_mat(0.0, 4.0, 0.0) * \
               avango.gua.make_rot_mat(beta, 0, 1, 0) * \
               avango.gua.make_rot_mat(90, 1, 0, 0)

        self.coordinate_system_1 = self.loader.create_geometry_from_file('coordinate_system_1',
                                                                         'data/objects/coordinate_system.obj',
                                                                         avango.gua.LoaderFlags.LOAD_MATERIALS)
        self.coordinate_system_1.Transform.value = mat1
        self.apply_material_uniform_recursively(
            self.coordinate_system_1, 'Emissivity', 0.25)
        self.apply_material_uniform_recursively(
            self.coordinate_system_1, 'Roughness', 0.8)
        self.scenegraph.Root.value.Children.value.append(
            self.coordinate_system_1)

        self.coordinate_system_2 = self.loader.create_geometry_from_file('coordinate_system_2',
                                                                         'data/objects/coordinate_system.obj',
                                                                         avango.gua.LoaderFlags.LOAD_MATERIALS)
        self.coordinate_system_2.Transform.value = mat2
        self.apply_material_uniform_recursively(
            self.coordinate_system_2, 'Emissivity', 0.25)
        self.apply_material_uniform_recursively(
            self.coordinate_system_2, 'Roughness', 0.8)
        self.scenegraph.Root.value.Children.value.append(
            self.coordinate_system_2)

    # builds the remaining parts of the scenegraph required to visualize two rotating monkeys
    def build_rotating_monkeys(self):
        # create big_monkey
        self.big_monkey = self.loader.create_geometry_from_file('big_monkey',
                                                                'data/objects/monkey.obj',
                                                                avango.gua.LoaderFlags.DEFAULTS)
        self.big_monkey.Material.value.set_uniform('Emissivity', 0.25)
        self.big_monkey.Material.value.set_uniform('Roughness', 0.8)
        self.big_monkey.Material.value.set_uniform(
            'Color', avango.gua.Vec4(1.0, 0.95, 0.55, 1.0))
        self.big_monkey.Material.value.EnableBackfaceCulling.value = False
        
        animator = RotationAnimator()

        # YOUR CODE - BEGIN (Exercise 1.5 - Node Structure for big_monkey)
        self.big_monkey.Transform.value = avango.gua.make_trans_mat(0.0, 3.0, -12.0) * \
                                          avango.gua.make_rot_mat(45, 0, 1, 0) * \
                                          avango.gua.make_scale_mat(2.5)
        self.scenegraph.Root.value.Children.value.append(self.big_monkey)
        # YOUR CODE - END (Exercise 1.5 - Node Structure for big_monkey)

        # YOUR CODE - BEGIN (Exercise 1.6 - Field Connection)
        # ...
        # YOUR CODE - END (Exercise 1.6 - Field Connection)

        # create another_big_monkey
        self.another_big_monkey = self.loader.create_geometry_from_file('another_big_monkey',
                                                                        'data/objects/monkey.obj',
                                                                        avango.gua.LoaderFlags.DEFAULTS)
        self.another_big_monkey.Material.value.set_uniform('Emissivity', 0.25)
        self.another_big_monkey.Material.value.set_uniform('Roughness', 0.8)
        self.another_big_monkey.Material.value.set_uniform(
            'Color', avango.gua.Vec4(1.0, 0.95, 0.55, 1.0))
        self.another_big_monkey.Material.value.EnableBackfaceCulling.value = False

        # YOUR CODE - BEGIN (Exercise 1.7 - Node Structure for another_big_monkey)
        self.another_big_monkey.Transform.value = avango.gua.make_trans_mat(8.0, 1.5, 0.0) * \
                                                  avango.gua.make_scale_mat(2.5)
        self.scenegraph.Root.value.Children.value.append(self.another_big_monkey)
        # YOUR CODE - END (Exercise 1.7 - Node Structure for another_big_monkey)
        

# Field Container taking the rotation speed as input and outputting an animated rotation matrix
class RotationAnimator(avango.script.Script):
    
    # input field
    sf_rot_mat = avango.gua.SFMatrix4()
    sf_rot_mat.value = avango.gua.make_identity_mat()

    def __init__(self):
        self.super(RotationAnimator).__init__()
        self.lf_time = time.time()
        self.always_evaluate(True)

    # called every frame because of self.always_evaluate(True)
    def evaluate(self):
        self.sf_rot_mat.value = avango.gua.make_rot_mat(0.1, 0, 1, 0) * \
                                self.sf_rot_mat.value


# Field Container taking a scenegraph node and computing its world transformation every frame
class WorldTransformComputer(avango.script.Script):
    
    # input field
    sf_node = avango.gua.SFNode()

    def __init__(self):
        self.super(WorldTransformComputer).__init__()
        self.always_evaluate(True)

    def compute_world_transform(self, node):
        # YOUR CODE - BEGIN (Exercise 1.8 - Compute World Transformation)
        pass
        # YOUR CODE - END (Exercise 1.8 - Compute World Transformation)

    # called every frame because of self.always_evaluate(True)
    def evaluate(self):
        if self.sf_node.value.WorldTransform.value != self.compute_world_transform(self.sf_node.value):
            print("Warning: World transform computation not correct.")

        # YOUR CODE - BEGIN (Exercise 1.9 - Matrix Decomposition)
        # ...
        # YOUR CODE - END (Exercise 1.9 - Matrix Decomposition)
