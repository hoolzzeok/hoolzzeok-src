"""EPSG:5174 (Korean 1985 / Modified Central Belt, Bessel, 지방행정 인허가 좌표) → WGS84 위경도. pyproj 없이 계산."""
import math
A=6377397.155; F=1/299.1528128; E2=F*(2-F)
LAT0=math.radians(38.0); LON0=math.radians(127.0028902777778); K0=1.0; X0=200000.0; Y0=500000.0
TOWGS=(-115.80,474.99,674.11,1.16,-2.31,-1.63,6.43)   # EPSG:5174 proj 정의의 towgs84
def _m(phi):
    e2=E2; e4=e2*e2; e6=e4*e2
    return A*((1-e2/4-3*e4/64-5*e6/256)*phi-(3*e2/8+3*e4/32+45*e6/1024)*math.sin(2*phi)+(15*e4/256+45*e6/1024)*math.sin(4*phi)-(35*e6/3072)*math.sin(6*phi))
def tm_inverse(x,y):
    M=_m(LAT0)+(y-Y0)/K0
    mu=M/(A*(1-E2/4-3*E2**2/64-5*E2**3/256)); e1=(1-math.sqrt(1-E2))/(1+math.sqrt(1-E2))
    p=mu+(3*e1/2-27*e1**3/32)*math.sin(2*mu)+(21*e1**2/16-55*e1**4/32)*math.sin(4*mu)+(151*e1**3/96)*math.sin(6*mu)+(1097*e1**4/512)*math.sin(8*mu)
    ep2=E2/(1-E2); C1=ep2*math.cos(p)**2; T1=math.tan(p)**2; N1=A/math.sqrt(1-E2*math.sin(p)**2); R1=A*(1-E2)/(1-E2*math.sin(p)**2)**1.5
    D=(x-X0)/(N1*K0)
    lat=p-(N1*math.tan(p)/R1)*(D**2/2-(5+3*T1+10*C1-4*C1**2-9*ep2)*D**4/24+(61+90*T1+298*C1+45*T1**2-252*ep2-3*C1**2)*D**6/720)
    lon=LON0+(D-(1+2*T1+C1)*D**3/6+(5-2*C1+28*T1-3*C1**2+8*ep2+24*T1**2)*D**5/120)/math.cos(p)
    return lat,lon
def to_ecef(lat,lon,a,e2,h=0):
    N=a/math.sqrt(1-e2*math.sin(lat)**2)
    return ((N+h)*math.cos(lat)*math.cos(lon),(N+h)*math.cos(lat)*math.sin(lon),(N*(1-e2)+h)*math.sin(lat))
def from_ecef(X,Y,Z,a,e2):
    lon=math.atan2(Y,X); p=math.hypot(X,Y); lat=math.atan2(Z,p*(1-e2))
    for _ in range(8):
        N=a/math.sqrt(1-e2*math.sin(lat)**2); lat=math.atan2(Z+e2*N*math.sin(lat),p)
    return lat,lon
def to_wgs84(x,y):
    lat,lon=tm_inverse(float(x),float(y))
    X,Y,Z=to_ecef(lat,lon,A,E2)
    dx,dy,dz,rx,ry,rz,s=TOWGS; sec=math.pi/(180*3600); rx*=sec; ry*=sec; rz*=sec; s=1+s*1e-6
    X2=dx+s*(X-rz*Y+ry*Z); Y2=dy+s*(rz*X+Y-rx*Z); Z2=dz+s*(-ry*X+rx*Y+Z)   # position vector (proj towgs84 기본)
    aw=6378137.0; fw=1/298.257223563; e2w=fw*(2-fw)
    la,lo=from_ecef(X2,Y2,Z2,aw,e2w)
    return round(math.degrees(la),6), round(math.degrees(lo),6)
if __name__=="__main__":
    print(to_wgs84(159394.946266179,-27270.643383592))   # 서귀포 중정로91번길 18 → 약 33.249, 126.56 이어야 함
    print(to_wgs84(198056.0,452440.0))                    # 서울 시청 근처 대략 검사
