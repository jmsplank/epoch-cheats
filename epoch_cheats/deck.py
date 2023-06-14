from typing import Literal

from pydantic import BaseModel


class Constant(BaseModel):
    qe: float
    mu0: float
    kb: float
    pi: float
    mp: float
    B0: float
    n0: float
    wci: float
    va: float
    di: float
    beta: float
    T0: float
    inflow: float
    thBn: float
    ppc: float
    E0: float
    amp: float
    sigma: float


class Control(BaseModel):
    nx: float
    ny: float
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    nsteps: float
    t_end: float
    dt_multiplier: float
    stdout_frequency: float
    use_current_correction: Literal["T", "F"]


class Hybrid(BaseModel):
    use_hybrid: Literal["T", "F"]
    electron_temperature_constant: str
    uniform_resistivity: float
    b_substeps: float
    e_smooth_iterations: float
    e_smooth_filter_width: float


class Boundaries(BaseModel):
    bc_x_min: float
    bc_x_max: str
    bc_y_min: str
    bc_y_max: str


class Fields(BaseModel):
    bx: float
    by: float
    ez: float


class Species(BaseModel):
    name: str
    charge: float
    mass: float
    nparticles: float
    number_density: float
    temp: str
    drift_x: float


class Injector(BaseModel):
    boundary: float
    species: str
    number_density: float
    temp: str
    drift_x: float
    npart_per_cell: float


class Output(BaseModel):
    dt_snapshot: float
    grid: str
    ex: str
    ey: str
    ez: str
    bx: str
    by: str
    bz: str
    jx: str
    jy: str
    jz: str
    average_particle_energy: str
    mass_density: str
    charge_density: str
    number_density: str
    temperature: str
    average_px: str
    average_py: str
    distribution_functions: str
    full_dump_every: float
    particles: str
    particle_weight: str
    id: str


class DistFn(BaseModel):
    name: str
    ndims: float
    dumpmask: str
    direction1: str
    direction2: str
    range1: str
    range2: str
    resolution1: float
    resolution2: float
    include_species: str


class Deck(BaseModel):
    constant: Constant
    control: Control
    hybrid: Hybrid
    boundaries: Boundaries
    fields: Fields
    species: Species
    injector: Injector
    output: Output
    dist_fn: DistFn
