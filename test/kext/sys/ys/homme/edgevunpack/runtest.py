# runtest.py
# 
import os
import sys
import glob
import shutil
from kext_sys_ys_homme_test import KExtSysYSHommeTest


class Test(KExtSysYSHommeTest):

    def generate(self, myname, result):

        workdir = result['mkdir_task']['workdir']
        tmpsrc = result['download_task']['tmpsrc']
        blddir = result['config_task']['blddir']

        srcfile = '%s/src/share/prim_advection_mod.F90'%tmpsrc
        mpipath = '/ncar/opt/intel/12.1.0.233/impi/4.0.3.008/intel64/include'
        namepath = 'prim_advection_mod:euler_step:edgevunpack'
        fc_flags = '-assume byterecl -fp-model precise -ftz -O3 -g -openmp'
        passed, out, err = self.extract_kernel(srcfile, namepath, workdir, \
            _I='%s/src:%s/src/share:%s/test_execs/perfTest:%s'%(tmpsrc, tmpsrc, blddir, mpipath), \
            _e='exclude.ini', \
            _D='HAVE_CONFIG_H', \
            __invocation='10:50', \
            __timing='repeat=1', \
            __mpi='ranks=0:10', \
            __kernel_compile='FC="ifort",FC_FLAGS="%s"'%fc_flags, \
            __outdir=workdir)

        result[myname]['stdout'] = out
        result[myname]['stderr'] = err

        if passed:
            result[myname]['statefiles'] = ['edgevunpack.10.0', 'edgevunpack.10.10', 'edgevunpack.50.0', 'edgevunpack.50.10']
            self.set_status(result, myname, self.PASSED)
        else:
            result[myname]['statefiles'] = []
            self.set_status(result, myname, self.FAILED, 'STDOUT: %s\nSTDERR: %s'%(out, err))

        return result

    def replace(self, myname, result):

        workdir = result['mkdir_task']['workdir']
        tmpsrc = result['download_task']['tmpsrc']

        for instrumented in glob.glob('%s/state/*.F90'%workdir):
            fname = os.path.basename(instrumented)
            if not os.path.exists('%s/src/share/%s.kgen'%(tmpsrc, fname)): 
                shutil.copy2('%s/src/share/%s'%(tmpsrc, fname), '%s/src/share/%s.kgen'%(tmpsrc, fname))
            os.remove('%s/src/share/%s'%(tmpsrc, fname))
            shutil.copy2(instrumented, '%s/src/share'%tmpsrc)
 
        self.set_status(result, myname, self.PASSED)

        return result

if __name__ == "__main__":
    # we may allow to run this test individually
    print('Please do not run this script from command line. Instead, run this script through KGen Test Suite .')
    print('Usage: cd ${KGEN_HOME}/test; ./kgentest.py')
    sys.exit(-1)