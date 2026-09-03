# Examples

`data/photonics_wg17_spectral_sweep.csv` is the first SMR photonics validation
fixture. It contains three synthetic repeats across nine wavelength points with
input/output optical power. Its JSON sidecar supplies source classification,
raw-source digest, a `ParsedSeriesCandidate` column mapping, a confirmation that
targets the exact candidate revision, sample, instruments, conditions,
timestamps, two independent state axes, and expected validation checks. The
`repeat` coordinate is an index, not a physical quantity.

The fixture is deliberately synthetic and must not be cited as experimental
evidence. Transmission and loss are absent from the raw CSV; implementations may
derive them only through explicit, provenance-linked operations.

The CSV plus sidecar form an M0/M2 test-fixture contract. Keeping a fixture in M0
does not move CSV import implementation out of M2.
