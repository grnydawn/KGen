import sys
from kapp_sys_ys_calc_test import KAppSysYSCalcTest

class Test(KAppSysYSCalcTest):
    def generate(self, myname, result):

        workdir = result['mkdir_task']['workdir']
        tmpsrc = result['download_task']['tmpsrc']


        srcfile = '%s/update_mod.F90'%tmpsrc
        namepath = 'update_mod:update:calc'
        fc_flags = '-O3'
        passed, out, err = self.extract_kernel(srcfile, namepath, \
            '"cd %s; make clean; make build"'%tmpsrc, \
            '"cd %s; make run"'%tmpsrc, \
            __invocation='0:0-1:1-2,0:2-3:3', \
            __timing='repeat=10', \
            __openmp='enable', \
            __outdir=workdir)

            #__debug='printvar=:i,:j,:output',

        result[myname]['stdout'] = out
        result[myname]['stderr'] = err
        result[myname]['datadir'] = '%s/data'%workdir

        if passed:
            result[myname]['statefiles'] = ['calc.0.0.1', 'calc.0.0.2', 'calc.0.1.1', 'calc.0.1.2', \
                'calc.0.2.3', 'calc.0.3.3']
            self.set_status(result, myname, self.PASSED)
        else:
            result[myname]['statefiles'] = []
            self.set_status(result, myname, self.FAILED, 'STDOUT: %s\nSTDERR: %s'%(out, err))

        return result

if __name__ == "__main__":
    # we may allow to run this test individually
    print('Please do not run this script from command line. Instead, run this script through KGen Test Suite .')
    print('Usage: cd ${KGEN_HOME}/test; ./kgentest.py')
    sys.exit(-1)