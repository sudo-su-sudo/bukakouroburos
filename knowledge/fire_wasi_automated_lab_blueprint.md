# Fire-WASI Automated Lab + Polygon Benchmark Blueprint
# Compounded 2026-10-24. Zero-brief for future cycles building executable evaluation harnesses.

## First-Principles Insight
An "Automated Lab" + "Benchmark" feedback loop is exactly an Online Judge (OJ) architecture scaled to R&D. Deconstruct existing OJs rather than inventing from scratch.

## Canonical Components (from DMOJ / Judge0 / Codeforces Polygon)
1. Web/API front for submission
2. Message queue (decouples submission from execution)
3. Judge Worker fleet (the actual Lab)
4. Persistent store for problems + results

## Isolation Technologies Ranked by Suitability
| Paradigm          | Implementation | Isolation Boundary     | Best For                          | Key Trade-off                  |
|-------------------|----------------|------------------------|-----------------------------------|--------------------------------|
| Micro-VM          | Firecracker    | Hardware (KVM)         | High-security, full-OS, I/O-heavy | Pre-boot block devices only   |
| User-space Kernel | gVisor         | Syscall ABI            | Network-bound multi-tenant        | High I/O overhead             |
| Capability API    | WASI/Wasmtime  | Explicit capability injection | Provably safe, in-memory pure functions | No ambient authority          |

## Emergent Architecture: Fire-WASI Hybrid
- **Macro layer**: Firecracker microVM per agent session / R&D pivot. API-driven, boots in ms, immutable clean-room.
- **Micro layer**: Inside the VM run a WASI runtime. Agent code compiles to .wasm. Host injects only the exact capabilities needed (stdin/stdout pipes, specific files, simulation handles).
- Dual sandbox: exploit must break both WASI capability model and KVM boundary.

## Benchmark as Polygon Problem Package
A benchmark is not static data. It is three programs:
1. **Generator**: programmatically creates test environment / simulation parameters (PyBullet world, ns-3 topology, SimPy processes, etc.).
2. **Validator**: enforces constraints on the generated environment.
3. **Checker**: runs the agent's code inside the simulation, observes final state, returns pass/fail (or richer metrics).

Supports both agentic modes:
- **Breadth (AlphaCode-style)**: spin 10k parallel Firecracker VMs, mount read-only rootfs + agent .wasm, get single pass/fail bit, destroy. High-throughput sampling.
- **Depth (Devin-style)**: one persistent Firecracker VM. WASI pipes give the agent a live interactive shell + real-time stderr feedback loop for multi-step debugging.

## How future cycles use this
- When building any evaluation harness, scoring tool, or outward experiment runner: start from this blueprint.
- Prefer Fire-WASI over plain Docker/ containers for untrusted agent code.
- Define every new research milestone's success criteria as a Polygon-style Problem Package so it is executable and versionable.

## Source
User-uploaded "Hacker-Minded Automated Lab Research.pdf", compounded 2026-10-24.
