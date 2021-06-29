PI = 3.141592
iSteps = 16
jSteps = 8
from math import *
from libs.vector import Vec3, Vec2


#Vec3 r0, Vec3 rd, sr
def rsi(r0, rd, sr):
    # ray-sphere intersection that assumes
    # the sphere is centered at the origin.
    # No intersection when result.x > result.y
    a = rd.dot(rd)
    b = 2.0 * rd.dot(r0)
    c = r0.dot(r0) - (sr * sr)
    d = (b*b) - 4.0*a*c
    if (d < 0.0):
        return Vec2(1e5,-1e5)
    return Vec2(
        (-b - sqrt(d))/(2.0*a),
        (-b + sqrt(d))/(2.0*a)
    )


#Vec3 r, Vec3 r0, Vec3 pSun, iSun, rPlanet, rAtmos, Vec3 kRlh, kMie, shRlh, shMie, g
def atmosphere(r, r0, pSun, iSun, rPlanet, rAtmos, kRlh, kMie, shRlh, shMie, g):
    # Normalize the sun and view directions.
    pSun = pSun.normalize()
    r = r.normalize()

    # Calculate the step size of the primary ray. Vec2
    p = rsi(r0, r, rAtmos)
    
    if p.x > p.y:
        return Vec3(0,0,0)
    
    p.y = min(p.y, rsi(r0, r, rPlanet).x)
    iStepSize = (p.y - p.x) / float(iSteps)

    # Initialize the primary ray time.
    iTime = 0.0

    # Initialize accumulators for Rayleigh and Mie scattering.
    totalRlh = Vec3(0,0,0)
    totalMie = Vec3(0,0,0)

    # Initialize optical depth accumulators for the primary ray.
    iOdRlh = 0.0
    iOdMie = 0.0

    # Calculate the Rayleigh and Mie phases.
    mu = r.dot(pSun)
    mumu = mu * mu
    gg = g * g
    pRlh = 3.0 / (16.0 * PI) * (1.0 + mumu)
    pMie = 3.0 / (8.0 * PI) * ((1.0 - gg) * (mumu + 1.0)) / (pow(1.0 + gg - 2.0 * mu * g, 1.5) * (2.0 + gg))

    # Sample the primary ray.
    for i in range(iSteps) :

        # Calculate the primary ray sample position.
        iPos = r0 + r * (iTime + iStepSize * 0.5)

        # Calculate the height of the sample.
        iHeight = iPos.abs() - rPlanet

        # Calculate the optical depth of the Rayleigh and Mie scattering for this step.
        odStepRlh = exp(-iHeight / shRlh) * iStepSize
        odStepMie = exp(-iHeight / shMie) * iStepSize

        # Accumulate optical depth.
        iOdRlh += odStepRlh
        iOdMie += odStepMie

        # Calculate the step size of the secondary ray.
        jStepSize = rsi(iPos, pSun, rAtmos).y / float(jSteps)

        # Initialize the secondary ray time.
        jTime = 0.0

        # Initialize optical depth accumulators for the secondary ray.
        jOdRlh = 0.0
        jOdMie = 0.0

        # Sample the secondary ray.
        for j in range(jSteps):

            # Calculate the secondary ray sample position.
            jPos = iPos + pSun * (jTime + jStepSize * 0.5)

            # Calculate the height of the sample.
            jHeight = jPos.abs() - rPlanet

            # Accumulate the optical depth.
            jOdRlh += exp(-jHeight / shRlh) * jStepSize
            jOdMie += exp(-jHeight / shMie) * jStepSize

            # Increment the secondary ray time.
            jTime += jStepSize


        # Calculate attenuation.
        attn = exp(-(kMie * (iOdMie + jOdMie) + kRlh * (iOdRlh + jOdRlh)))

        # Accumulate scattering.
        totalRlh += odStepRlh * attn
        totalMie += odStepMie * attn

        # Increment the primary ray time.
        iTime += iStepSize



    # Calculate and return the final color.
    return iSun * (pRlh * kRlh * totalRlh + pMie * kMie * totalMie)

class Atmo:
    model =