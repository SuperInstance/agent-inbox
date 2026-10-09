# Node join protocol — zero-touch lanes

**Law (2026-10-08):** a new node joins with self-healing on day one, never
after a failure. No lane may depend on a human retyping a command. The HP
lane died because its tunnel was a one-shot manual `ssh -R` with no
supervision; a laptop sleep or WSL reset killed it permanently.

## Join checklist (run once, on the node)
1. Generate the node's keypair: `ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519`
2. Register the public key BOTH places from an already-trusted machine:
   - Oracle `~/.ssh/authorized_keys` (for the tunnel)
   - GitHub repo deploy keys, write access (for pushes)
   - Verify with `ssh-keygen -l` fingerprint comparison — never trust a
     photo transcription of base64.
3. Install the supervised tunnel (survives drops, restarts, reboots):
   `autossh -M 0 -N -f -R <port>:localhost:22 -o ServerAliveInterval=30 -o ServerAliveCountMax=3 ubuntu@147.224.38.131`
   plus the `@reboot` crontab line running the same.
4. Verify from Oracle: the port answers on Oracle's loopback
   (`/dev/tcp/127.0.0.1/<port>`). Tunnels terminate on ORACLE, not on
   the Muse VM — never check the VM's localhost.
5. Confirm the lane in the inbox: drop a `hello` task, watch it claim.

## Port assignments (Oracle loopback)
- 2222 = proart (GPU)
- 2223 = kimi (cloud research)
- 2224 = hp (experiment box)

## When a lane goes dark
1. Check Oracle's ports first. Dark ≠ dead — the inbox is the tasking
   mechanism; workers pull from GitHub regardless of tunnels.
2. If the port is closed >1h and the node has no self-healing, the join
   was defective — fix the join, don't ask the human to retype.
3. Reroute the work before routing the human: reassign the inbox task
   to a live lane. Zero-input is the hard constraint.
