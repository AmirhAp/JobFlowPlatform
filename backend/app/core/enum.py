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

