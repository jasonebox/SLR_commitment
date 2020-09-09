pro destripe_alb_500m_daily_PP;,fday,plt
;
;fday=152
;plt=0
;plt=1

discrete_text='c'

plt=1
;iday=fday-8
iday=267
fday=300

min_n_thresh=3

collection=['5','6']
colx=1

iyear=2000 & fyear=2019
n_years=fyear-iyear+1.
year=strtrim(fix(indgen(n_years)+iyear),2)

;print,'enter year 0, 2 digits'
;read,yearchoice0
;print,'enter year 1, 2 digits'
;read,yearchoice1

yearchoice0=19
yearchoice1=19

ni=7200 & nj=7200

not_NRT=1 ; 0 for NRT

close,/all

ancpath='~/Dropbox/MOD10A1/NRT/prog/ancil/'

scaling_factor=0.18
scaling_factor=0.1
sf=scaling_factor

if plt then begin
  set_plot,'x'
  device,decomposed=0
  xsize=ni*scaling_factor & ysize=nj*scaling_factor
  window,0,xsize=xsize,ysize=ysize
  !order=1
endif

maskx=bytarr(7200,7200)
file='~/Dropbox/500m_grid/2016_7200x7200.byt'
openr,1,file
readu,1,maskx
close,1
ice=where(maskx gt 0,c_clever)
;print,c_clever
;stop
;!order=1
;loadct,4,/silent
;tvscl,congrid(maskx,ni*sf,nj*sf)
;print,c_clever
;;rdpix,congrid(maskx,ni*sf,nj*sf)
;stop

;print,c_clever/1.e6
;stop

maskx=0

n_days=365
mind=indgen(n_days)+1

minds=strmid(strtrim(mind+1000,2),1,3)
;print,minds
;stop
n_segments=n_elements(mind)

for yy=yearchoice0,yearchoice1 do begin
;for yy=13,18 do begin
;for yy=15,14,-1 do begin
;for yy=15,0,-1 do begin
;  print,year
;  print,yy

base_dir='/Volumes/LaCie'
;base_dir='/Volumes/Tb2'
;base_dir='~'
path=base_dir+'/0_dat/MOD10A1/500m.'+collection(colx)+'/'+year(yy)+'/'
outpath=base_dir+'/0_dat/MOD10A1/500m_d.'+collection(colx)+'/'+year(yy)+'/'

spawn,'mkdir '+base_dir+'0_dat/MOD10A1/500m_d.'+collection(colx)+'/'

spawn,'mkdir '+outpath

print,outpath

for j=iday,fday do begin
;for j=60,182 do begin
  print,year(yy)

msg='ls '+path+' >/tmp/list'+discrete_text+'.txt'
;print,msg
spawn,msg
;spawn,'cat /tmp/list.txt'
n=file_lines('/tmp/list'+discrete_text+'.txt')
;print,n
;stop

openr,1,'/tmp/list'+discrete_text+'.txt'
file=strarr(n)
readf,1,file
close,1

days=(strmid(file,5,3)) ; this will compain of type conversion error unless the term after file, is lined up to the 3 digit day of year
;print,days
;stop


print,'-------------------------------------------- processing day ',j

valid_days=where(days ge mind(j)-5 and days le mind(j)+5,c_valid_days)

;print,c_valid_days
;stop
if c_valid_days gt 2 then begin

;print
print,'using :',days(valid_days),' N: ',c_valid_days

;print,'using :'+file(valid_days)
;spawn,'ls -lF '+file(valid_days)
;stop
a=fltarr(c_valid_days,c_clever)


for i=0,c_valid_days-1 do begin

;  print,' populate array',c_valid_days-i,' '+file(valid_days(i))
  
  spawn,'ls -lF '+path+file(valid_days(i))
  temp=intarr(c_clever)
  openr,1,path+file(valid_days(i))
  readu,1,temp
  close,1

;temp2=float(temp)
;print,min(temp2),max(temp2)  
;stop
b=intarr(ni,nj)
b(ice)=temp(*)

;loadct,4,/silent
;scaling_factor=0.15
;set_plot,'x'
;device,decomposed=0
;xsize=ni*scaling_factor & ysize=nj*scaling_factor
;window,0,xsize=xsize,ysize=ysize
;!order=1
;x=congrid(b*0.01,xsize,ysize)
;tvscl,x
;rdpix,x
;stop
;wait,1

conversion_factor=0.01

  ;b*=0.1
;conversion_factor=1.
  a(i,*)=b(ice)*conversion_factor
  ;a(i,*)=b(ice)*0.01
;if plt then  plot,a(i,*),psym=3,charsize=3,title=year(yy)+' '+strtrim(days(valid_days(i)),2)
;stop
endfor ; i
;stop
b=0
albedo_mean_multi_day=fltarr(c_clever)
deviations_temp=fltarr(c_clever)
threshs_temp=fltarr(c_clever)
devs_post_filter_temp=fltarr(c_clever)
n_temp=bytarr(c_clever)
tossed=bytarr(c_clever)

;print,'begin number krumpin, http://www.youtube.com/watch?v=yrZLCCjIZc8'


;print,c_clever
;stop

;for i=double(3200000),double(3800000) do begin
for i=double(0),double(c_clever)-1 do begin ; i is each pixel on ice
  thresh=0.15 
  valid=where(a(*,i) gt 0. and a(*,i) lt 1.,c)
  if c gt min_n_thresh then begin ; min_n_thresh is minimum number of days
    x=fltarr(c) ; c is the number of valid days
    x(*)=a(valid,i) ; convert albedo to a decimal and float
    medianx=median(x) ; median of valid days
    deviations=abs((x-medianx)/medianx) ; x is the array of valid days, how they depart from a median in a fractional sense
    deviations_temp(i)=stdev(deviations); pre-filtering stdev, only a diagnostic, not required
   ; threshs_temp(i)=thresh ; not used
    good=where(deviations lt thresh,cc) ; good is array elements that are under a variance threshold
    if cc gt min_n_thresh then begin
      albedo_mean_multi_day(i)=mean(x(good)) ; finally the acceptable albedo is the average of cases under the acceptable variance threshold
      devs_post_filter_temp(i)=stdev(deviations(good)) ; post-filtering stdev
      n_temp(i)=c ; counts
    endif
    bad=where(deviations ge thresh,cc)
    tossed(i)=cc
  endif
endfor ; i
;if plt then begin
;  !p.multi=0
;  plot,albedo_mean_multi_day,psym=3,ystyle=9,/ylog,yrange=[0.1,1.1]
;;wait,6
;endif

a=0

;valid=where(medians gt 0 and medians lt 100)
;maskx=bytarr(ni,nj)
;maskx(valid)=1
;openw,1,ancpath+'land_ice_byte_7200x7200_all.img'
;writeu,1,maskx
;close,1
;stop

;help,ni,nj

ns=bytarr(ni,nj)
ns(ice)=n_temp(*)

temp=fltarr(ni,nj)
temp(ice)=albedo_mean_multi_day(*)

;tvscl,congrid(temp,ni*sf,nj*sf)

;file=outpath+year(yy)+'.'+strtrim(strtrim(minds(j-1),2),2)+'_500m_MOD10A1_alb_7200x7200'
v=where(fix(days) eq j,c)
;print,c
file=outpath+year(yy)+'.'+days(v(0))
print,file
openw,1,file;+'.img'
writeu,1,fix(temp(ice)*10000)
close,1
;stop
du=0

if du then begin
  
loadct,4,/silent
x=congrid(temp,xsize,ysize)
tvscl,x
;rdpix,x
;stop

print,'Writing '+file

file=outpath+year(yy)+'.'+days(v(0))+'_devs';+'_500m_MOD10A1_alb_7200x7200_clever'
openw,1,file;+'.img'
writeu,1,deviations_temp
close,1
deviations_temp=0

file=outpath+year(yy)+'.'+days(v(0))+'_threshs';+'_500m_MOD10A1_alb_7200x7200_clever'
openw,1,file;+'.img'
writeu,1,threshs_temp
close,1
threshs_temp=0

file=outpath+year(yy)+'.'+days(v(0))+'_devs_post_filter';+'_500m_MOD10A1_alb_7200x7200_clever'
openw,1,file;+'.img'
writeu,1,devs_post_filter_temp
close,1
devs_post_filter_temp=0

file=outpath+year(yy)+'.'+days(v(0))+'_tossed';+'_500m_MOD10A1_alb_7200x7200_clever'
openw,1,file;+'.img'
writeu,1,tossed
close,1
tossed=0

;openw,1,outpath+year(yy)+'_Albedo_std-post_'+strtrim(minds(j),2)+input_res+'.img'
;writeu,1,devs_post_filter
;close,1
;devs=0
;
;openw,1,outpath+year(yy)+'_Albedo_n-cases_'+strtrim(minds(j),2)+input_res+'.img'
;writeu,1,ns
;close,1
;ns=0
;
;endif ; wo_anc_state
endif ; du

; clear memory
a=0
medians=0

endif ; sufficient number of segments

endfor ; j? segments

endfor ; yy

print,'Done'

regrid_daily_500m_to_pp,fday,plt

end
