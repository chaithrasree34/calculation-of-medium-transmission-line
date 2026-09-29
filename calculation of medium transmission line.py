# calculation-of-medium-transmission-line
import cmath
import math

print("==========================================")
print(" MEDIUM TRANSMISSION LINE - NOMINAL PI")
print("==========================================")

# Input data
Vr_kV = float(input("Enter receiving-end line voltage (kV): "))
Ir = float(input("Enter receiving-end current (A): "))
pf = float(input("Enter receiving-end power factor (0 to 1): "))
length = float(input("Enter line length (km): "))

R_per_km = float(input("Enter resistance per km per phase (ohm/km): "))
X_per_km = float(input("Enter reactance per km per phase (ohm/km): "))
C_per_km = float(input("Enter capacitance per km per phase (microF/km): "))

frequency = float(input("Enter frequency (Hz): "))

# ------------------------------------------
# Receiving-end quantities
# ------------------------------------------

Vr_line = Vr_kV * 1000
Vr_phase = Vr_line / math.sqrt(3)

# Power factor angle
phi = math.acos(pf)

# Assume lagging power factor
Ir_complex = Ir * cmath.exp(-1j * phi)

# ------------------------------------------
# Total series impedance and shunt admittance
# ------------------------------------------

R = R_per_km * length
X = X_per_km * length

Z = complex(R, X)

# Capacitance
C = C_per_km * 1e-6 * length

# Angular frequency
omega = 2 * math.pi * frequency

# Shunt admittance
Y = 1j * omega * C

# ------------------------------------------
# Nominal-pi ABCD parameters
# ------------------------------------------

A = 1 + (Y * Z) / 2
B = Z * (1 + (Y * Z) / 4)
C_abcd = Y * (1 + (Y * Z) / 4)
D = A

# ------------------------------------------
# Sending-end voltage and current
# ------------------------------------------

Vs_phase = A * Vr_phase + B * Ir_complex

Is_complex = C_abcd * Vr_phase + D * Ir_complex

Vs_line = abs(Vs_phase) * math.sqrt(3)
Is = abs(Is_complex)

# ------------------------------------------
# Sending-end power
# ------------------------------------------

S_sending = 3 * Vs_phase * Is_complex.conjugate()

P_sending = S_sending.real
Q_sending = S_sending.imag

S_sending_mag = abs(S_sending)

pf_sending = abs(P_sending) / S_sending_mag

# ------------------------------------------
# Receiving-end power
# ------------------------------------------

P_receiving = (
    math.sqrt(3)
    * Vr_line
    * Ir
    * pf
)

S_receiving = (
    math.sqrt(3)
    * Vr_line
    * Ir
)

# ------------------------------------------
# Voltage regulation
# ------------------------------------------

voltage_regulation = (
    (Vs_line - Vr_line) / Vr_line
) * 100

# ------------------------------------------
# Power loss
# ------------------------------------------

power_loss = P_sending - P_receiving

# ------------------------------------------
# Efficiency
# ------------------------------------------

efficiency = (
    P_receiving / P_sending
) * 100

# ------------------------------------------
# Display results
# ------------------------------------------

print("\n==========================================")
print(" RESULTS")
print("==========================================")

print(f"Total resistance       : {R:.4f} ohm/phase")
print(f"Total reactance        : {X:.4f} ohm/phase")
print(f"Total capacitance      : {C * 1e6:.4f} microF/phase")
print(f"Series impedance (Z)   : {Z:.4f} ohm")
print(f"Shunt admittance (Y)   : {Y:.6e} S")

print("\n--- ABCD PARAMETERS ---")
print(f"A = {A:.6f}")
print(f"B = {B:.6f}")
print(f"C = {C_abcd:.6e}")
print(f"D = {D:.6f}")

print("\n--- TRANSMISSION LINE RESULTS ---")
print(f"Sending-end voltage    : {Vs_line / 1000:.4f} kV")
print(f"Sending-end current    : {Is:.4f} A")
print(f"Sending-end power      : {P_sending / 1000:.4f} kW")
print(f"Sending-end power factor: {pf_sending:.4f}")

print(f"\nReceiving-end power    : {P_receiving / 1000:.4f} kW")
print(f"Power loss             : {power_loss / 1000:.4f} kW")
print(f"Voltage regulation     : {voltage_regulation:.4f} %")
print(f"Efficiency             : {efficiency:.4f} %")
