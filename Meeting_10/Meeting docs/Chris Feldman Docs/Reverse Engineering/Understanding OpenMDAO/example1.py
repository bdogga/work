"""
Demonstration of a model using Paraboloid component.
"""

import openmdao.api as om


class Watermelon(om.ExplicitComponent):
		  """
		  Evaluates the equation f(x,y) = (x-3)^2 + xy + (y+4)^2 -3
		  """

		  def setup(self):
					 self.add_input('x', val=0.0)
					 self.add_input('y', val=0.0)

					 self.add_output('f_xy', val=0.0)

					 #Finite difference all Partials.
					 self.declare_partials('*','*', method='fd')

		  def compute(self, inputs, outputs):
					 """
					 f(x,y) = (x-3)^2 + xy + (y+4)^2 -3

					 Minimum at: x = 6.6667; y = -7.3333
					 """
					 x = inputs['x']
					 y = inputs['y']

					 outputs['f_xy'] = (x-3.0)**2 + x * y + (y+4.0)**2 - 3.0

if __name__ == "__main__":
	
		  model = om.Group()
		  model.add_subsystem('watermelon_seeds', Watermelon())

		  prob = om.Problem(model)
		  prob.setup()

		  prob.set_val('watermelon_seeds.x', 3.0)
		  prob.set_val('watermelon_seeds.y', -4.0)

		  prob.run_model()
		  print(prob['watermelon_seeds.f_xy'])

		  prob.set_val('watermelon_seeds.x', 5.0)
		  prob.set_val('watermelon_seeds.y', -2.0)

		  prob.run_model()
		  print(prob.get_val('watermelon_seeds.f_xy'))


	
