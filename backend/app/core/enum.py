from enum import Enum


#this in this way:
# saved -> applied -> interview -> offered/rejected -> closed
class PostStatus(str, Enum):
    SAVED = "saved"
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFERED = "offered"
    REJECTED = "rejected"
    CLOSED = "closed"


#user flow :
# saved -> massaged -> need_action/need_response -> massaged/done
class PersonStatus(str, Enum):
    SAVED = "saved"
    CONTACTED = "contacted"
    NEED_ACTION = "need_action"
    NEED_RESPONSE = "need_response"
    DONE = "done"