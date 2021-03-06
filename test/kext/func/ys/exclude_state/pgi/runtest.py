# runtest.py
# 
from kext_func_ys_exclude_state_test import KExtFuncYSESTTest

class CustomTest(KExtFuncYSESTTest):
    def config(self, myname, result):

        result[myname]['FC'] = 'pgfortran'
        result[myname]['FC_FLAGS'] = ''
        result[myname]['PRERUN'] = 'module purge; module try-load ncarenv/1.0; module try-load ncarbinlibs/1.1; module try-load ncarcompilers/1.0; module try-load pgi/16.1'

        self.set_status(result, myname, self.PASSED)

        return result

if __name__ == "__main__":
    print('Please do not run this script from command line. Instead, run this script through KGen Test Suite .')
    print('Usage: cd ${KGEN_HOME}/test; ./kgentest.py')
    sys.exit(-1)
