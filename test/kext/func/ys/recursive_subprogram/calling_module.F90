module calling_module

        USE kernel, only : add

        public calling_subroutine

        contains

        subroutine calling_subroutine()

                real(kind=4), dimension(2,2) :: ar1, ar2, ar3

                ar1(:,:) = 1.0
                ar2(:,:) = 1.0
                ar3(:,:) = 0.0

                call add(ar1, ar2, ar3, 4)

                print *, "ar3 =", ar3

        end subroutine

end module
