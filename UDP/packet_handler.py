import actions
import consensus


def packet_handler():
    pass


def send_action(id):
    pcktID = consensus.decode_pcktID(id)

    action = {
        consensus.PcktID.hello_c2s: actions.SYN_send(),
        consensus.PcktID.hello_back_s2c: actions.SYN_ACK(),
        consensus.PcktID.vote_c2s_request_vote: actions.VoteRequest(),
        consensus.PcktID.vote_s2c_broadcast_question: actions.VoteBroadcast(),
        consensus.PcktID.vote_c2s_response_to_question: actions.VoteResponse(),
        consensus.PcktID.vote_s2c_broadcast_result: actions.ResultBroadcast(),
    }

    return action.get(pcktID, "Unknown PcktID")
