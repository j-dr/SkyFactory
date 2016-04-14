# SkyFactory
Set up and run large suites of mock sky simulations.

## Finding Outputs
1. Outputs for a given simulation go to the global output dir in the system config file, followed by the 
  simulation name, followed by the simulation number like this `{global output dir}/{sim name}-{sim number}`.
2. Outputs for a given task always go to the global output dir for the sim from 1 followed by the task name in 
  in all lower case (i.e., `{global output dir}/{sim name}-{sim number}/calcrnn` for task `CalcRnn`).

## Notes on Adding New Tasks
1. Make a file for the task under `templates/{taskname}.py`
2. In the file from 1, make a child class of `BaseTemplate` which looks like
  ```python
  from .basetemplate import BaseTemplate
  
  class MyTask(BaseTemplate):
      def write_config(self, data_output_path, box_size):
          """
          write the job configs
          
          write job config to self.sysparams['JobBase']
          any outputs go to data_output_path
          """

      def write_jobscript(self, data_output_path, box_size):
          """
          write the job submission script
          
          write job submission script to self.sysparams['JobBase']
          outputs got to data_output_path
          """
  ```
  If you need to run the task only once, instead of for all N-body boxes, add the following to code above
  ```python
      def __init__(self, simnum, system, cosmo):
          super(DensMap, self).__init__(simnum, system, cosmo, allboxes=True)
  ```
3. Make sure to import the class from 2 in `templates/__init__.py`
4. Make sure to write and put your job submission script in `systems/{all systems}/MyTask.{Sched}` 
  where `{Sched}` is the corresponding parameter in the `{system}.yaml` file.
4. Make sure to add task to `setup_sky.py` script
