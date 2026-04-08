# FreeSWITCH notes

Use `mod_event_socket` for control-plane orchestration.
Use SIP profile + external gateway for actual trunk connectivity.
For production:
- enable ACLs instead of exposing ESL broadly
- separate RTP/media and signaling networks
- configure call recording policies per compliance rules
- set CPS / concurrent channel limits
- tune retry windows for RNR and reschedules
