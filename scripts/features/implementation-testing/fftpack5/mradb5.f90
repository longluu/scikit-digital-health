! -*- f90 -*-
subroutine mradb5 ( m, ido, l1, cc, im1, in1, ch, im2, in2, &
  wa1, wa2, wa3, wa4 )

!*****************************************************************************80
!
!! MRADB5 is an FFTPACK5 auxiliary routine.
!
!  License:
!
!    Licensed under the GNU General Public License (GPL).
!    Copyright (C) 1995-2004, Scientific Computing Division,
!    University Corporation for Atmospheric Research
!
!  Modified:
!
!    27 March 2009
!
!  Author:
!
!    Paul Swarztrauber
!    Richard Valent
!
!  Reference:
!
!    Paul Swarztrauber,
!    Vectorizing the Fast Fourier Transforms,
!    in Parallel Computations,
!    edited by G. Rodrigue,
!    Academic Press, 1982.
!
!    Paul Swarztrauber,
!    Fast Fourier Transform Algorithms for Vector Computers,
!    Parallel Computing, pages 45-63, 1984.
!
!  Parameters:
!
  implicit none

  integer ( kind = 4 ) ido
  integer ( kind = 4 ) in1
  integer ( kind = 4 ) in2
  integer ( kind = 4 ) l1

  real ( kind = 4 ) arg
  real ( kind = 4 ) cc(in1,ido,5,l1)
  real ( kind = 4 ) ch(in2,ido,l1,5)
  integer ( kind = 4 ) i
  integer ( kind = 4 ) ic
  integer ( kind = 4 ) idp2
  integer ( kind = 4 ) im1
  integer ( kind = 4 ) im2
  integer ( kind = 4 ) k
  integer ( kind = 4 ) m
  integer ( kind = 4 ) m1
  integer ( kind = 4 ) m1d
  integer ( kind = 4 ) m2
  integer ( kind = 4 ) m2s
  real ( kind = 4 ) ti11
  real ( kind = 4 ) ti12
  real ( kind = 4 ) tr11
  real ( kind = 4 ) tr12
  real ( kind = 4 ) wa1(ido)
  real ( kind = 4 ) wa2(ido)
  real ( kind = 4 ) wa3(ido)
  real ( kind = 4 ) wa4(ido)

  m1d = ( m - 1 ) * im1 + 1
  m2s = 1 - im2
  arg = 2.0E+00 * 4.0E+00 * atan ( 1.0E+00 ) / 5.E+00
  tr11 = cos ( arg )
  ti11 = sin ( arg )
  tr12 = cos ( 2.0E+00 * arg )
  ti12 = sin ( 2.0E+00 * arg )

  do k = 1, l1
    m2 = m2s
    do m1 = 1, m1d, im1
      m2 = m2 + im2
      ch(m2,1,k,1) = cc(m1,1,1,k) + 2.0E+00 * cc(m1,ido,2,k) &
        + 2.0E+00 * cc(m1,ido,4,k)
      ch(m2,1,k,2) = ( cc(m1,1,1,k) + tr11 * 2.0E+00 * cc(m1,ido,2,k) &
        + tr12 * 2.0E+00 * cc(m1,ido,4,k) ) - ( ti11 * 2.0E+00 * cc(m1,1,3,k) &
        + ti12 * 2.0E+00 * cc(m1,1,5,k) )
      ch(m2,1,k,3) = ( cc(m1,1,1,k) + tr12 * 2.0E+00 * cc(m1,ido,2,k) &
        + tr11 * 2.0E+00 * cc(m1,ido,4,k) ) - ( ti12 * 2.0E+00 * cc(m1,1,3,k) &
        - ti11 * 2.0E+00 * cc(m1,1,5,k) )
      ch(m2,1,k,4) = ( cc(m1,1,1,k) + tr12 * 2.0E+00 * cc(m1,ido,2,k) &
        + tr11 * 2.0E+00 * cc(m1,ido,4,k) ) + ( ti12 * 2.0E+00 * cc(m1,1,3,k) &
        - ti11 * 2.0E+00 * cc(m1,1,5,k) )
      ch(m2,1,k,5) = ( cc(m1,1,1,k) + tr11 * 2.0E+00 * cc(m1,ido,2,k) &
        + tr12 * 2.0E+00 * cc(m1,ido,4,k) ) + ( ti11 * 2.0E+00 * cc(m1,1,3,k) &
        + ti12 * 2.0E+00 * cc(m1,1,5,k) )
    end do
  end do

  if ( ido == 1 ) then
    return
  end if

  idp2 = ido + 2
  do k = 1, l1
    do i = 3, ido, 2
      ic = idp2 - i
      m2 = m2s
      do m1 = 1, m1d, im1
        m2 = m2 + im2
        ch(m2,i-1,k,1) = cc(m1,i-1,1,k)+(cc(m1,i-1,3,k)+cc(m1,ic-1,2,k)) &
          +(cc(m1,i-1,5,k)+cc(m1,ic-1,4,k))
        ch(m2,i,k,1) = cc(m1,i,1,k)+(cc(m1,i,3,k)-cc(m1,ic,2,k)) &
          +(cc(m1,i,5,k)-cc(m1,ic,4,k))
        ch(m2,i-1,k,2) = wa1(i-2)*((cc(m1,i-1,1,k)+tr11* &
          (cc(m1,i-1,3,k)+cc(m1,ic-1,2,k))+tr12 &
          *(cc(m1,i-1,5,k)+cc(m1,ic-1,4,k)))-(ti11*(cc(m1,i,3,k) &
          +cc(m1,ic,2,k))+ti12*(cc(m1,i,5,k)+cc(m1,ic,4,k)))) &
          -wa1(i-1)*((cc(m1,i,1,k)+tr11*(cc(m1,i,3,k)-cc(m1,ic,2,k)) &
          +tr12*(cc(m1,i,5,k)-cc(m1,ic,4,k)))+(ti11*(cc(m1,i-1,3,k) &
          -cc(m1,ic-1,2,k))+ti12*(cc(m1,i-1,5,k)-cc(m1,ic-1,4,k))))
        ch(m2,i,k,2) = wa1(i-2)*((cc(m1,i,1,k)+tr11*(cc(m1,i,3,k) &
          -cc(m1,ic,2,k))+tr12*(cc(m1,i,5,k)-cc(m1,ic,4,k))) &
          +(ti11*(cc(m1,i-1,3,k)-cc(m1,ic-1,2,k))+ti12 &
          *(cc(m1,i-1,5,k)-cc(m1,ic-1,4,k)))) + wa1(i-1) &
          *((cc(m1,i-1,1,k)+tr11*(cc(m1,i-1,3,k) &
          +cc(m1,ic-1,2,k))+tr12*(cc(m1,i-1,5,k)+cc(m1,ic-1,4,k))) &
          -(ti11*(cc(m1,i,3,k)+cc(m1,ic,2,k))+ti12 &
          *(cc(m1,i,5,k)+cc(m1,ic,4,k))))
        ch(m2,i-1,k,3) = wa2(i-2) &
          *((cc(m1,i-1,1,k)+tr12*(cc(m1,i-1,3,k)+cc(m1,ic-1,2,k)) &
          +tr11*(cc(m1,i-1,5,k)+cc(m1,ic-1,4,k)))-(ti12*(cc(m1,i,3,k) &
          +cc(m1,ic,2,k))-ti11*(cc(m1,i,5,k)+cc(m1,ic,4,k)))) &
          -wa2(i-1) &
          *((cc(m1,i,1,k)+tr12*(cc(m1,i,3,k)- &
        cc(m1,ic,2,k))+tr11*(cc(m1,i,5,k)-cc(m1,ic,4,k))) &
          +(ti12*(cc(m1,i-1,3,k)-cc(m1,ic-1,2,k))-ti11 &
          *(cc(m1,i-1,5,k)-cc(m1,ic-1,4,k))))
        ch(m2,i,k,3) = wa2(i-2) &
          *((cc(m1,i,1,k)+tr12*(cc(m1,i,3,k)- &
          cc(m1,ic,2,k))+tr11*(cc(m1,i,5,k)-cc(m1,ic,4,k))) &
          +(ti12*(cc(m1,i-1,3,k)-cc(m1,ic-1,2,k))-ti11 &
          *(cc(m1,i-1,5,k)-cc(m1,ic-1,4,k)))) &
          + wa2(i-1) &
          *((cc(m1,i-1,1,k)+tr12*(cc(m1,i-1,3,k)+cc(m1,ic-1,2,k)) &
          +tr11*(cc(m1,i-1,5,k)+cc(m1,ic-1,4,k)))-(ti12*(cc(m1,i,3,k) &
          +cc(m1,ic,2,k))-ti11*(cc(m1,i,5,k)+cc(m1,ic,4,k))))
        ch(m2,i-1,k,4) = wa3(i-2) &
          *((cc(m1,i-1,1,k)+tr12*(cc(m1,i-1,3,k)+cc(m1,ic-1,2,k)) &
          +tr11*(cc(m1,i-1,5,k)+cc(m1,ic-1,4,k)))+(ti12*(cc(m1,i,3,k) &
          +cc(m1,ic,2,k))-ti11*(cc(m1,i,5,k)+cc(m1,ic,4,k)))) &
          -wa3(i-1) &
          *((cc(m1,i,1,k)+tr12*(cc(m1,i,3,k)- &
          cc(m1,ic,2,k))+tr11*(cc(m1,i,5,k)-cc(m1,ic,4,k))) &
          -(ti12*(cc(m1,i-1,3,k)-cc(m1,ic-1,2,k))-ti11 &
          *(cc(m1,i-1,5,k)-cc(m1,ic-1,4,k))))
        ch(m2,i,k,4) = wa3(i-2) &
          *((cc(m1,i,1,k)+tr12*(cc(m1,i,3,k)- &
          cc(m1,ic,2,k))+tr11*(cc(m1,i,5,k)-cc(m1,ic,4,k))) &
          -(ti12*(cc(m1,i-1,3,k)-cc(m1,ic-1,2,k))-ti11 &
          *(cc(m1,i-1,5,k)-cc(m1,ic-1,4,k)))) &
          + wa3(i-1) &
          *((cc(m1,i-1,1,k)+tr12*(cc(m1,i-1,3,k)+cc(m1,ic-1,2,k)) &
          +tr11*(cc(m1,i-1,5,k)+cc(m1,ic-1,4,k)))+(ti12*(cc(m1,i,3,k) &
          +cc(m1,ic,2,k))-ti11*(cc(m1,i,5,k)+cc(m1,ic,4,k))))
        ch(m2,i-1,k,5) = wa4(i-2) &
          *((cc(m1,i-1,1,k)+tr11*(cc(m1,i-1,3,k)+cc(m1,ic-1,2,k)) &
          +tr12*(cc(m1,i-1,5,k)+cc(m1,ic-1,4,k)))+(ti11*(cc(m1,i,3,k) &
          +cc(m1,ic,2,k))+ti12*(cc(m1,i,5,k)+cc(m1,ic,4,k)))) &
          -wa4(i-1) &
          *((cc(m1,i,1,k)+tr11*(cc(m1,i,3,k)-cc(m1,ic,2,k)) &
          +tr12*(cc(m1,i,5,k)-cc(m1,ic,4,k)))-(ti11*(cc(m1,i-1,3,k) &
          -cc(m1,ic-1,2,k))+ti12*(cc(m1,i-1,5,k)-cc(m1,ic-1,4,k))))
        ch(m2,i,k,5) = wa4(i-2) &
          *((cc(m1,i,1,k)+tr11*(cc(m1,i,3,k)-cc(m1,ic,2,k)) &
          +tr12*(cc(m1,i,5,k)-cc(m1,ic,4,k)))-(ti11*(cc(m1,i-1,3,k) &
          -cc(m1,ic-1,2,k))+ti12*(cc(m1,i-1,5,k)-cc(m1,ic-1,4,k)))) &
          + wa4(i-1) &
          *((cc(m1,i-1,1,k)+tr11*(cc(m1,i-1,3,k)+cc(m1,ic-1,2,k)) &
          +tr12*(cc(m1,i-1,5,k)+cc(m1,ic-1,4,k)))+(ti11*(cc(m1,i,3,k) &
          +cc(m1,ic,2,k))+ti12*(cc(m1,i,5,k)+cc(m1,ic,4,k))))
      end do
    end do
  end do

  return
end
