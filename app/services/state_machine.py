from transitions import Machine

class CallFlowMachine:
    states = [
        "NEW",
        "DIALING",
        "CONNECTED",
        "CONSENT_PENDING",
        "DISCLOSURE_PENDING",
        "NIL_DISCLOSURE_DONE",
        "ROUTE_TO_IMU",
        "RNR",
        "RESCHEDULED",
        "COMPLETED",
        "FAILED",
    ]

    def __init__(self, initial: str = "NEW"):
        self.machine = Machine(model=self, states=self.states, initial=initial, ignore_invalid_triggers=True)
        self.machine.add_transition("dial", "NEW", "DIALING")
        self.machine.add_transition("connect", "DIALING", "CONNECTED")
        self.machine.add_transition("ask_consent", "CONNECTED", "CONSENT_PENDING")
        self.machine.add_transition("consent_ok", "CONSENT_PENDING", "DISCLOSURE_PENDING")
        self.machine.add_transition("nil_done", "DISCLOSURE_PENDING", "NIL_DISCLOSURE_DONE")
        self.machine.add_transition("escalate", ["DISCLOSURE_PENDING", "CONSENT_PENDING"], "ROUTE_TO_IMU")
        self.machine.add_transition("mark_rnr", ["DIALING", "CONNECTED"], "RNR")
        self.machine.add_transition("reschedule", ["CONNECTED", "DISCLOSURE_PENDING"], "RESCHEDULED")
        self.machine.add_transition("complete", ["NIL_DISCLOSURE_DONE", "ROUTE_TO_IMU"], "COMPLETED")
        self.machine.add_transition("fail", "*", "FAILED")
