 program geomturbo
! program to create the geomturbo file....Kiran Siddappaji 12/22/2010
! Added the splitter capability...Ahmed Nemnem
! inputs: 3dbgbinput file, 3Dsection files...modified (6/26/12)
! inputs: number of airfoil coordinate points. Should be the same as 2D Airfoil coordinates.
!output: geomturbo file
! command: geomturbo [3dbgbinput.#.dat] [np]
 
	implicit none

	character*32 fname,fname1,fname2,fname3,temp,case
	character*32 ibrowc,fext
	character*3 npoints
	integer iap,nspn,nrow,row,clmn,nblade,np,k,nx,nax,ia,i
	integer row_n,ibrow,nsp(50),number_of_splitters,unit_adjustment

	logical :: exist

	parameter(nrow=1,row = 600,clmn = 20)
	parameter(nx=500,nax=50)

	real bsf
	real xb(nx,nax),yb(nx,nax),zb(nx,nax)
	real xb1(nx,nax),yb1(nx,nax),zb1(nx,nax)
	real xs(nx,nax),ys(nx,nax),zs(nx,nax)! suction side coordinates
	real xp(nx,nax),yp(nx,nax),zp(nx,nax)! pressure side coordinates
	real zhub(row),rhub(row),tempr1(2)
	real ztip(row),rtip(row)
	!------ scaled coordinates
	real xs_scaled(nx,nax),ys_scaled(nx,nax),zs_scaled(nx,nax)! suction side coordinates
	real xp_scaled(nx,nax),yp_scaled(nx,nax),zp_scaled(nx,nax)! pressure side coordinates
	real zhub_scaled(row),rhub_scaled(row)
	real ztip_scaled(row),rtip_scaled(row),trarray(3)
	real xm(nx,nax),rm(nx,nax)

call getarg(1,fname3)
call getarg(2,npoints)
read(npoints,*)np
!
! Welcome message
call displayMessage

! check if there is a splitter file in the folder to add its definition:
k = index(fname3,'.')
number_of_splitters = 0
fname1 = fname3(1:k+1)//'S'//'.dat'
inquire(file=fname1, exist= exist )
if (exist) then 
	number_of_splitters = 1
	print*
	print*, 'Splitter file detected ...'
endif

!---opening the input file---
write(*,*)
write(*,*) 'Reading inputs from 3dbgbinput file and sec#.dat files'
write(*,*)

! Read input file:
call readfile (fname3,ibrowc,fext,ibrow,row_n,nblade,bsf,nspn,nsp,xm,rm,number_of_splitters,unit_adjustment)
write(*,*)
write(*,*)'Writing geomturbo file..'
write(*,*)
write(temp,*)row_n
if (number_of_splitters.ne.0) then
	fname='row_wth_splitter.'//trim(adjustl(temp))//'.geomTurbo'
else
	fname='row.'//trim(adjustl(temp))//'.geomTurbo'
endif
open(1,file=fname,status='unknown')
write(1,*)'GEOMETRY TURBO'
write(1,*)'VERSION ',5.3
write(1,*)'TOLERANCE',1e-006
write(1,*)'NI_BEGIN CHANNEL'
write(1,*)' NI_BEGIN basic_curve'
write(1,*)'  NAME     hub'
write(1,*)'  DISCRETISATION',10
write(1,*)'  DATA_REDUCTION',0
write(1,*)'  NI_BEGIN zrcurve'
write(1,*)'   ZR'

!---------------
! Remove the zero radius and double points (bulb autogrid case):
k = 0
do i=1,nsp(1)
	!print*,'rm(i,1) ',rm(i,1)
	if (rm(i,1) <= 1.0E-06) then
		rm(i,1) = 0
		k = k+1
		continue
	else
        k = 1
    endif
enddo
nsp(1) = nsp(1)-(k-1)
!---------------

write(1,*),   nsp(1) !  no. of hub and tip coordinates
do i=k,nsp(1)+(k-1)
		write(1,*)bsf*xm(i,1),bsf*rm(i,1)
enddo
!
write(1,*)'  NI_END zrcurve'
write(1,*)' NI_END basic_curve'
write(1,*)' NI_BEGIN basic_curve'
write(1,*)'  NAME     shroud'
write(1,*)'  DISCRETISATION',10
write(1,*)'  DATA_REDUCTION',0
write(1,*)'  NI_BEGIN zrcurve'
write(1,*)'   ZR'
write(1,*),   nsp(nspn)
do i=1,nsp(nspn)
   write(1,*)bsf*xm(i,nspn),bsf*rm(i,nspn)
enddo
close(5)
write(1,*)'  NI_END zrcurve'
write(1,*)' NI_END basic_curve'
write(1,*)' NI_BEGIN channel_curve hub'
write(1,*)'   NAME     hub'
write(1,*)'   VERTEX     CURVE_P hub',0
write(1,*)'   VERTEX     CURVE_P hub',1
write(1,*)' NI_END channel_curve hub'
write(1,*)' NI_BEGIN channel_curve shroud'
write(1,*)'   NAME     shroud'
write(1,*)'   VERTEX     CURVE_P shroud',0
write(1,*)'   VERTEX     CURVE_P shroud',1
write(1,*)' NI_END channel_curve shroud'
write(1,*)' NI_BEGIN channel_curve nozzle'
write(1,*)'   NAME     nozzle'
write(1,*)' NI_END channel_curve nozzle'
write(1,*)'NI_END CHANNEL'
write(1,*)'NI_BEGIN nirow'
write(1,*)'   NAME     row ',row_n
write(1,*)'   TYPE       normal'
write(1,*)'   PERIODICITY',nblade
write(1,*)'NI_BEGIN NINonAxiSurfaces  hub'
write(1,*)'   NAME     non axisymmetric hub'
write(1,*)'   REPETITION',0
write(1,*)'NI_END NINonAxiSurfaces  hub'
write(1,*)'NI_BEGIN NINonAxiSurfaces  shroud'
write(1,*)'   NAME     non axisymmetric shroud'
write(1,*)'   REPETITION',0
write(1,*)'NI_END NINonAxiSurfaces  shroud'
!----------------------------------------------next lines repreated in case of splitter
write(1,*)'NI_BEGIN NIBlade'
write(1,*)'   NAME     Main Blade'
write(1,*)'NI_BEGIN nibladegeometry'
write(1,*)'                TYPE     GEOMTURBO'
write(1,*)'                GEOMETRY_MODIFIED',0
write(1,*)'GEOMETRY TURBO VERSION 5'
write(1,*)'blade_expansion_factor_hub',0.01! This is just a sample value
write(1,*)'blade_expansion_factor_shroud',0.01 
write(1,*)'intersection_npts',10
write(1,*)'intersection_control',1
write(1,*)'data_reduction',0
write(1,*)'data_reduction_spacing_tolerance',0.0001
write(1,*)'data_Reduction_angle_tolerance',90
write(1,*)'control_points_distribution     0 -1 -1 -1 -1 -1 -1'
write(1,*)'units',1
write(1,*)'number_of_blades',nblade
write(1,*)'suction'
write(1,*)'SECTIONAL'
write(1,*)nspn
!
write(ibrowc,'(i3)')row_n
print*,'bladerow:',ibrowc
! reading the section files....
if(mod(np,2).eq.0)then ! even number of airfoil points.
  np = np-1
  write(*,*)
  print*, "**************** ERROR *******************"
  print*, "Airfoil has even number of coordinates."
  print*, "Airfoil needs odd number of coordinates..."
  print*, "Add one more point or remove one."
  print*, "**************** ERROR *******************"
  stop 
endif  
do ia = 1,nspn
   write(temp,*)ia
   fname3='sec'//trim(adjustl(temp))//'.'//trim(fext)//'.dat'
   open(3,file=fname3,status='unknown')
   do i=1,np
      read(3,*)xb1(i,ia),yb1(i,ia),zb1(i,ia)
      xb(i,ia) = xb1(i,ia)/unit_adjustment
      yb(i,ia) = yb1(i,ia)/unit_adjustment
      zb(i,ia) = zb1(i,ia)/unit_adjustment
   enddo
!
! Assigning the points as suction and pressure side points...
!d o ia=1,nspn  
   do i=(np+1)/2,1,-1
      xs(i,ia)=xb(i,ia)
      ys(i,ia)=yb(i,ia)
      zs(i,ia)=zb(i,ia)
   enddo
   do i=(np+1)/2,np
      xp(i,ia)=xb(i,ia)
      yp(i,ia)=yb(i,ia)
      zp(i,ia)=zb(i,ia)
   enddo
!
!do ia=1,nspn
   write(1,*)'#   section',ia
   write(1,*)'XYZ'
   write(1,*)(np+1)/2
   do i=(np+1)/2,1,-1
     write(1,*)zs(i,ia),-ys(i,ia),xs(i,ia)
   enddo
   close(3)
enddo
!
write(1,*)'pressure'
write(1,*)'SECTIONAL'
write(1,*)nspn
do ia=1,nspn
  write(1,*)'#   section',ia
  write(1,*)'XYZ'
  write(1,*)(np+1)/2
  do i=(np+1)/2,np
    write(1,*)zp(i,ia),-yp(i,ia),xp(i,ia)
  enddo
enddo
write(1,*)'NI_END    nibladegeometry'
write(1,*)'   SOLID_BODY_CONFIGURATION',0
write(1,*)'NI_END    NIBlade'
!-----------------------------------------------
if (number_of_splitters.ne.0) then
		write(1,*)'NI_BEGIN NIBlade'
		write(1,*)'   NAME     Splitter1'
		write(1,*)'NI_BEGIN nibladegeometry'
		write(1,*)'                TYPE     GEOMTURBO'
		write(1,*)'                GEOMETRY_MODIFIED',0
		write(1,*)'GEOMETRY TURBO VERSION 5'
		write(1,*)'blade_expansion_factor_hub',0.01! This is just a sample value
		write(1,*)'blade_expansion_factor_shroud',0.01 
		write(1,*)'intersection_npts',10
		write(1,*)'intersection_control',1
		write(1,*)'data_reduction',0
		write(1,*)'data_reduction_spacing_tolerance',0.0001
		write(1,*)'data_Reduction_angle_tolerance',90
		write(1,*)'control_points_distribution     0 -1 -1 -1 -1 -1 -1'
		write(1,*)'units',1
		write(1,*)'number_of_blades',nblade
		write(1,*)'suction'
		write(1,*)'SECTIONAL'
		write(1,*)nspn
		!
		write(ibrowc,'(i3)')row_n
		print*,'splitters:',ibrowc
		! reading the section files....
		if(mod(np,2).eq.0)then ! even number of airfoil points.
		  np = np-1
		  write(*,*)
		  print*, "**************** ERROR *******************"
		  print*, "Airfoil has even number of coordinates."
		  print*, "Airfoil needs odd number of coordinates..."
		  print*, "Add one more point or remove one."
		  print*, "**************** ERROR *******************"
		  stop 
		endif  
		do ia = 1,nspn
		   write(temp,*)ia
		   fname3='sec'//trim(adjustl(temp))//'.'//trim(fext)//'S.dat'
		   open(3,file=fname3,status='unknown')
		   do i=1,np
			  read(3,*)xb1(i,ia),yb1(i,ia),zb1(i,ia)
			  xb(i,ia) = xb1(i,ia)/unit_adjustment
			  yb(i,ia) = yb1(i,ia)/unit_adjustment
			  zb(i,ia) = zb1(i,ia)/unit_adjustment
		   enddo
		!
		! Assigning the points as suction and pressure side points...
		!d o ia=1,nspn  
		   do i=(np+1)/2,1,-1
			  xs(i,ia)=xb(i,ia)
			  ys(i,ia)=yb(i,ia)
			  zs(i,ia)=zb(i,ia)
		   enddo
		   do i=(np+1)/2,np
			  xp(i,ia)=xb(i,ia)
			  yp(i,ia)=yb(i,ia)
			  zp(i,ia)=zb(i,ia)
		   enddo
		!
		!do ia=1,nspn
		   write(1,*)'#   section',ia
		   write(1,*)'XYZ'
		   write(1,*)(np+1)/2
		   do i=(np+1)/2,1,-1
			 write(1,*)zs(i,ia),-ys(i,ia),xs(i,ia)
		   enddo
		   close(3)
		enddo
		!
		write(1,*)'pressure'
		write(1,*)'SECTIONAL'
		write(1,*)nspn
		do ia=1,nspn
		  write(1,*)'#   section',ia
		  write(1,*)'XYZ'
		  write(1,*)(np+1)/2
		  do i=(np+1)/2,np
			write(1,*)zp(i,ia),-yp(i,ia),xp(i,ia)
		  enddo
		enddo
		write(1,*)'NI_END    nibladegeometry'
		write(1,*)'   SOLID_BODY_CONFIGURATION',0
		write(1,*)'NI_END    NIBlade'
endif

write(1,*)'NI_END    nirow'
write(1,*)'NI_END GEOMTURBO'
write(1,*)
write(1,*)'NI_BEGIN GEOMETRY'
write(1,*)'NI_END     GEOMETRY'
close(1)

print*,""
print*,"-----END-----"
end program geomturbo
!------------------------------------------------
      SUBROUTINE ASKI(PROMPT,IINPUT)
!
!---- integer input
!
      CHARACTER*(*) PROMPT
      integer IINPUT
!
      NP = INDEX(PROMPT,'^') - 1
      IF(NP.EQ.0) NP = LEN(PROMPT)
!
 10   WRITE(*,1000) PROMPT(1:NP)
      READ (*,*,ERR=10) IINPUT
      RETURN
!
 1000 FORMAT(/A,'   i>  ',$)
      END ! ASKI
!---------------------------------------------------
      subroutine askr(prompt,rinput)
!
!---- real input
!
      character*(*) prompt
      real rinput
!
      np = index(prompt,'^') - 1
      if(np.eq.0) np = len(prompt)
!
 10   write(*,1000) prompt(1:np)
      read (*,*,err=10) rinput
      return
!
 1000 format(/a,'   r>  ',$)
      end ! askr
!--------------------------------------------------------
	subroutine readfile(fname3,ibrowc,fext,ibrow,row_n,nblade,bsf,nspn,nsp,xm,rm,number_of_splitters,unit_adjustment)
	
	implicit none

	character*32 fname3,temp,case
	character*32 ibrowc,fext
    character(len=2) :: units
	integer iap,nspn,nblade,nx,nax,ia,i,unit_adjustment
	integer row_n,ibrow,nsp(50),number_of_splitters
	parameter(nx=500,nax=50)

	real bsf
	!------ scaled coordinates
	real trarray(3)
	real xm(nx,nax),rm(nx,nax)
	
	open(5,file=fname3,status='unknown')
	!---reading parameters from input file----
	read(5,*)temp
	! reading the casename
	read(5,*)fext
	  write(*,*)'case:',fext
	read(5,*)temp
	read(5,*)ibrow
	write(*,*)'bladerow #:',ibrow
	write(ibrowc,'(i3)')ibrow
	print*,ibrowc
	row_n=ibrow
	write(*,*)
	read(5,*)temp
	read(5,*)nblade ! number of blades in this row
	 if (number_of_splitters.ne.0) then
		 nblade=nblade/2
	 endif
	print*,'Number of blades in this row:',nblade
	read(5,'(A)'),temp
    units = temp((index(temp,'(')+1):(index(temp,')')-1))
	!units = temp(24:25)
	print*,'Input file units is ',units
	read(5,*)bsf
	!-----------------------
	unit_adjustment = 1
	if (units == 'mm') then
		bsf = bsf/1000
		unit_adjustment = 1000
	elseif (units == 'cm') then
		bsf = bsf/100
		unit_adjustment = 100
	endif
	!-------------------------
	write(*,*)'bsf in meters:',bsf
	write(*,*) 
	read(5,*)temp
	read(5,*)nspn
	print*,'Number of blade sections:',nspn
	write(*,*)
	read(5,*)temp
	read(5,*)temp
	read(5,*)temp
	!reading number of airfoil coordinates incase of a user defined airfoil from a file
	do while(temp.ne.'Airfoil')
	 read(5,*)temp
	enddo
	read(5,*)temp
	do while(temp.ne.'x_s')
	 read(5,*)temp
	! print*,'temp=',temp
	enddo
	do ia=1,nspn
	 nsp(ia) = 0
	 do while(.true.)
	  read(5,*)trarray(1),trarray(2)
	!  print*,trarray(1),trarray(2)
	  if(trarray(2).ne.0)then
	   nsp(ia) = nsp(ia) + 1
	   xm(nsp(ia),ia) = trarray(1)
	   rm(nsp(ia),ia) = trarray(2)
	! print*,xm(nsp(ia),ia),rm(nsp(ia),ia)
	  else
	   exit
	  endif
	 enddo
	enddo

end subroutine readfile
!----------------------------------------------
!---------------------------------------------------------
! Subroutine to display the welcome message
!---------------------------------------------------------
subroutine displayMessage

write(*,*)
write(*,*)'***********************************************************'
write(*,*)'***********************************************************'
write(*,*)'****  .geomTurbo file generator script                 ****'
write(*,*)'****                                                   ****'  
write(*,*)'****  Version 1.0                                      ****' 
write(*,*)'****                                                   ****'
write(*,*)'****  This software comes with ABSOLUTELY NO WARRANTY  ****'
write(*,*)'****                                                   ****'
write(*,*)'****  This is a program which generates a .geomTurbo   ****' 
write(*,*)'****  ...file for Numeca Autogrid tool...              ****'
write(*,*)'****                                                   ****'
write(*,*)'****  Inputs: 3dbgbinput file, sec*.casename.dat files ****' 
write(*,*)'****                                                   ****'
write(*,*)'****  Outputs: row.bladerownumber.geomTurbo            ****'
write(*,*)'****                                                   ****'
write(*,*)'****  ---------------by Kiran Siddappaji         ----  ****'
write(*,*)'****  ------------------- s2kn@mail.uc.edu       ----  ****'
write(*,*)'****  ---------------by Ahmed Nemnem             ----  ****'
write(*,*)'****  ------------------- nemnemam@mail.uc.edu   ----  ****'
write(*,*)'***********************************************************'
write(*,*)'***********************************************************'

return
end subroutine displayMessage
!---------------------------------------------------------
