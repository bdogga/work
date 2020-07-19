import openmdao.api as om
import numpy as np
import pandas as pd

from openmdao.utils.file_wrap import InputFileGenerator
from openmdao.utils.file_wrap import FileParser

writeParser = InputFileGenerator()
readParser = FileParser()


class BladeDesignOptimizerMDAO(om.ExternalCodeComp):

    def setup(self):
        
        #link inputs
        #self.add_input('dev')
        self.add_input('t')
        self.add_input('in_beta')
        self.add_input('out_beta')
        self.add_input('cur1')
        self.add_input('cur2')
        self.add_input('cur3')
        self.add_input('cur4')
        self.add_input('cur5')
        self.add_input('cur6')
        self.add_input('cur7')
        self.add_input('u_max')
        self.add_input('LE_radius')
        self.add_input('t_TE')
        self.add_input('dydxTE')
        
        #link outputs
        #self.add_output('S2')
        #self.add_output('zeta')
        self.add_output('Sq_diff')
        
        #setup filenames
        self.tbladeinputfilebase = '3dbgbinput.2.base'
        self.spancontrolfilebase = 'spancontrolinputs.2.base'

        self.tbladeinputfile = '3dbgbinput.2.dat'
        self.spancontrolfile = 'spancontrolinputs.2.dat'

       # self.S2outfile = 'S2_out.dat'
        #self.zetaoutfile = 'zeta_out.dat'
        self.Sq_diffoutfile = 'Sq_diff_out.dat'

        #self.options['external_input_files'] = [self.tbladeinputfile, self.spancontrolfile]
      #  self.options['external_output_files'] = [self.S2outfile, self.zetaoutfile]
        self.options['external_output_files'] = [self.Sq_diffoutfile]

        #setup run command
        self.options['command'] = ["bash", "run_least_squares.sh"]

#        self.timeout = 10

        #have openmdao calculate partial derivs 
        self.declare_partials(of='*', wrt='*', method='fd', step=0.00001)

    def compute(self,inputs,outputs):
        
        #dev = inputs['dev']
        t  = inputs['t']
        in_beta = inputs['in_beta']
        out_beta = inputs['out_beta']
        cur1 = inputs['cur1']
        cur2 = inputs['cur2']
        cur3 = inputs['cur3']
        cur4 = inputs['cur4']
        cur5 = inputs['cur5']
        cur6 = inputs['cur6']
        cur7 = inputs['cur7']
        LE_radius = inputs['LE_radius']
        u_max = inputs['u_max']
        t_TE = inputs['t_TE']
        dydxTE = inputs['dydxTE'] 
        #add c1..c6
        #add dy_dx_TE
        #LE_radius   u_max
        
        #write output files
        
         #Tblade file
        writeParser.set_template_file(self.tbladeinputfilebase)
        writeParser.set_generated_file(self.tbladeinputfile)
        writeParser.reset_anchor()
        writeParser.mark_anchor("Sectionwise")
        writeParser.transfer_var(in_beta[0], 2, 2)
        writeParser.transfer_var(in_beta[0], 3, 2)
        writeParser.generate()

#        writeParser.set_template_file(self.tbladeinputfilebase)
#        writeParser.set_generated_file(self.tbladeinputfile)
        writeParser.reset_anchor()
        writeParser.mark_anchor("Sectionwise")
        writeParser.transfer_var(out_beta[0], 2, 3)
        writeParser.transfer_var(out_beta[0], 3, 3)
        writeParser.generate()

        #spancontrol file
        writeParser.set_template_file(self.spancontrolfilebase)
        writeParser.set_generated_file(self.spancontrolfile)
        writeParser.reset_anchor()
        writeParser.mark_anchor("Span control points, Chord & curv")
        writeParser.transfer_var(cur1[0], 3, 7)
        writeParser.transfer_var(cur1[0], 4, 7)
        #writeParser.generate()
        
#        writeParser.set_template_file(self.spancontrolfilebase)
#        writeParser.set_generated_file(self.spancontrolfile)
        writeParser.reset_anchor()
        writeParser.mark_anchor("Span control points, Chord & curv")
        writeParser.transfer_var(cur2[0], 3, 8)
        writeParser.transfer_var(cur2[0], 4, 8)
        #writeParser.generate()

#        writeParser.reset_anchor()
#        writeParser.set_template_file(self.spancontrolfilebase)
#        writeParser.set_generated_file(self.spancontrolfile)
        writeParser.reset_anchor()
        writeParser.mark_anchor("Span control points, Chord & curv")
        writeParser.transfer_var(cur3[0], 3, 9)
        writeParser.transfer_var(cur3[0], 4, 9)
      #  writeParser.generate()

#        writeParser.set_template_file(self.spancontrolfilebase)
#        writeParser.set_generated_file(self.spancontrolfile)
        writeParser.reset_anchor()
        writeParser.mark_anchor("Span control points, Chord & curv")
        writeParser.transfer_var(cur4[0], 3, 10)
        writeParser.transfer_var(cur4[0], 4, 10)
       # writeParser.generate()

#        writeParser.set_template_file(self.spancontrolfilebase)
#        writeParser.set_generated_file(self.spancontrolfile)
        writeParser.reset_anchor()
        writeParser.mark_anchor("Span control points, Chord & curv")
        writeParser.transfer_var(cur5[0], 3, 11)
        writeParser.transfer_var(cur5[0], 4, 11)
      #  writeParser.generate()
    
#        writeParser.set_template_file(self.spancontrolfilebase)
#        writeParser.set_generated_file(self.spancontrolfile)
        writeParser.reset_anchor()
        writeParser.mark_anchor("Span control points, Chord & curv")
        writeParser.transfer_var(cur6[0], 3, 12)
        writeParser.transfer_var(cur6[0], 4, 12)
       # writeParser.generate()

#        writeParser.set_template_file(self.spancontrolfilebase)
#        writeParser.set_generated_file(self.spancontrolfile)
        writeParser.reset_anchor()
        writeParser.mark_anchor("Span control points, Chord & curv")
        writeParser.transfer_var(cur7[0], 3, 13)
        writeParser.transfer_var(cur7[0], 4, 13)
      #  writeParser.generate()

        #spancontrol file
        #writeParser.set_template_file(self.spancontrolfilebase)
        #writeParser.set_generated_file(self.spancontrolfile)
        writeParser.reset_anchor()
        writeParser.mark_anchor("Span control points, Chord & thick")
        writeParser.transfer_var(t[0], 3, 4)
        writeParser.transfer_var(t[0], 4, 4)
        writeParser.generate()

        writeParser.reset_anchor()
        writeParser.mark_anchor("Span control points, Chord & thick")
        writeParser.transfer_var(LE_radius[0], 3, 2)
        writeParser.transfer_var(LE_radius[0], 4, 2)
        writeParser.generate()

        writeParser.reset_anchor()
        writeParser.mark_anchor("Span control points, Chord & thick")
        writeParser.transfer_var(u_max[0], 3, 3)
        writeParser.transfer_var(u_max[0], 4, 3)
        writeParser.generate()

        writeParser.reset_anchor()
        writeParser.mark_anchor("Span control points, Chord & thick")
        writeParser.transfer_var(t_TE[0], 3, 5)
        writeParser.transfer_var(t_TE[0], 4, 5)
        writeParser.generate()
        
        writeParser.reset_anchor()
        writeParser.mark_anchor("Span control points, Chord & thick")
        writeParser.transfer_var(dydxTE[0], 3, 6)
        writeParser.transfer_var(dydxTE[0], 4, 6)
        writeParser.generate()
                        
        #execute
        super(BladeDesignOptimizerMDAO, self).compute(inputs,outputs)
        
        #Parse:
       # with open(self.S2outfile, 'r') as output_file:
        #    S2=float(output_file.read())
            
        #with open(self.zetaoutfile, 'r') as output_file:
        #    zeta=float(output_file.read())
        #with open(self.blade1outfile, 'r') as output_file:
         #    data = output_file.readlines()[3:]  
         #   data = pd.DataFrame(data)
         #    data = data.str.split(pat="  ") 
         #    print(data)
       # print("dev=",dev,", T=",t)
        with open(self.Sq_diffoutfile, 'r') as output_file:
            Sq_diff = float(output_file.read())
        print("T=",t)
        print("LE_radius=",LE_radius)
        print("u_max=",u_max)
        print("t_TE=",t_TE)
        print("in_beta=",in_beta)
        print("out_beta=",out_beta)
        print("cur1=",cur1)
        print("cur2=",cur2)
        print("cur3=",cur3)
        print("cur4=",cur4)
        print("cur5=",cur5)
        print("cur6=",cur6)
        print("cur7=",cur7)
        print("dydxTE=",dydxTE)
        print("Sq_diff=",Sq_diff)
        #print("zeta=",zeta,", S2=",S2)
        outputs['Sq_diff']=Sq_diff
       # outputs['S2'] = S2
       # outputs['zeta'] = zeta
        

if __name__ == "__main__":
    prob = om.Problem()
    
    model = prob.model

    indeps = prob.model.add_subsystem('indeps', om.IndepVarComp())
    
    #indeps.add_output('dev', -10.99)  #-12.99374745 
    indeps.add_output('t',0.1917708)#0.16109697)#0.10)   #0.991080592614
    indeps.add_output('LE_radius', 4.98620583)#5.01766249)#5.89894475)#5.9)
    indeps.add_output('u_max',0.3834332)#0.3312661)#0.40180786)#0.29)
    indeps.add_output('t_TE', 0.00061836)#0.03259426)#0.00023444)#0.00001)
    indeps.add_output('in_beta',4.48448514)#4.4698513)#0.0142108)#0.00001)
    indeps.add_output('out_beta',-4.5084396)#-4.49380167)#-0.01422172)#-0.00001)
    indeps.add_output('cur1', -0.64973656)#-0.54128768)#0.39996715)#0.4)
    indeps.add_output('cur2', 0.82803128)#0.91772727)#0.02998418)#0.03)
    indeps.add_output('cur3', 0.06193288)#-0.02567901)#-0.09996155)#-0.1)
    indeps.add_output('cur4', -0.20022772)#-0.40924999)#0.30007017)#0.3)
    indeps.add_output('cur5', 0.86500481)#0.85005146)#0.10006228)#0.1)
    indeps.add_output('cur6', -0.55109569)#-0.46763371)#0.02000394)#0.02)
    indeps.add_output('cur7', -0.97878055)#-0.92474029)#0.21000711)#0.21)
    indeps.add_output('dydxTE',-0.04423976)#-0.00597116)#-0.14570056)#0.0)
    
    model.add_subsystem('runblade', BladeDesignOptimizerMDAO())
    
    prob.driver = om.ScipyOptimizeDriver()
    prob.driver.options['optimizer'] = 'SLSQP'  

   # prob.model.connect('indeps.dev', 'runblade.dev')
    prob.model.connect('indeps.t', 'runblade.t')
    prob.model.connect('indeps.LE_radius', 'runblade.LE_radius')
    prob.model.connect('indeps.u_max', 'runblade.u_max')
    prob.model.connect('indeps.t_TE', 'runblade.t_TE')
    prob.model.connect('indeps.in_beta','runblade.in_beta')
    prob.model.connect('indeps.out_beta','runblade.out_beta')
    prob.model.connect('indeps.cur1', 'runblade.cur1')
    prob.model.connect('indeps.cur2', 'runblade.cur2')
    prob.model.connect('indeps.cur3', 'runblade.cur3')
    prob.model.connect('indeps.cur4', 'runblade.cur4')
    prob.model.connect('indeps.cur5', 'runblade.cur5')
    prob.model.connect('indeps.cur6', 'runblade.cur6')
    prob.model.connect('indeps.cur7', 'runblade.cur7')
    prob.model.connect('indeps.dydxTE', 'runblade.dydxTE')
    
    #prob.model.add_design_var('indeps.dev', lower=-15, upper=0, ref=10)
    prob.model.add_design_var('indeps.t', lower=1e-5, upper=0.8)
    prob.model.add_design_var('indeps.LE_radius',lower=0.00001, upper=5.9)
    prob.model.add_design_var('indeps.u_max', lower=0.2, upper=0.6)
    prob.model.add_design_var('indeps.t_TE', lower=0.00001, upper=0.001)
    prob.model.add_design_var('indeps.in_beta', lower=1e-5, upper=90)
    prob.model.add_design_var('indeps.out_beta', lower=-90, upper=-1e-5)
    prob.model.add_design_var('indeps.cur1', lower=-1, upper=1)
    prob.model.add_design_var('indeps.cur2', lower=-1, upper=1)
    prob.model.add_design_var('indeps.cur3', lower=-1, upper=1)
    prob.model.add_design_var('indeps.cur4', lower=-1, upper=1)
    prob.model.add_design_var('indeps.cur5', lower=-1, upper=1)
    prob.model.add_design_var('indeps.cur6', lower=-1, upper=1)
    prob.model.add_design_var('indeps.cur7', lower=-1, upper=1)
    prob.model.add_design_var('indeps.dydxTE', lower=-6, upper=0)

    
    #prob.model.add_constraint('runblade.S2',equals=-60.276)
    

    #prob.model.add_objective('runblade.zeta')
    prob.model.add_objective('runblade.Sq_diff')
    
    prob.driver.options['tol'] = 1e-3

    prob.setup()    

    #prob.run_model()
    prob.run_driver()
    
    #print("zeta=",prob['runblade.zeta'],", S2=",prob['runblade.S2'])
    print("Sq_diff=",prob['runblade.Sq_diff'])
    
