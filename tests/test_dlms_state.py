import pytest

from dlms_cosem import enumerations, state
from dlms_cosem.exceptions import LocalDlmsProtocolError
from dlms_cosem.protocol import acse
from dlms_cosem.protocol.acse import UserInformation
from dlms_cosem.protocol.xdlms import Conformance, InitiateRequestApdu


def test_non_aarq_on_initial_raises_protocol_error():
    s = state.DlmsConnectionState()

    with pytest.raises(LocalDlmsProtocolError):
        s.process_event(acse.ReleaseResponseApdu())


def test_aarq_makes_dlms_waiting_for_aare():
    s = state.DlmsConnectionState()
    s.process_event(
        acse.ApplicationAssociationRequestApdu(
            user_information=UserInformation(
                InitiateRequestApdu(proposed_conformance=Conformance())
            )
        )
    )
    assert s.current_state == state.AWAITING_ASSOCIATION_RESPONSE


def test_aare_sets_ready_on_waiting_aare_response():
    s = state.DlmsConnectionState(current_state=state.AWAITING_ASSOCIATION_RESPONSE)
    s.process_event(
        acse.ApplicationAssociationResponseApdu(
            enumerations.AssociationResult.ACCEPTED,
            result_source_diagnostics=enumerations.AcseServiceUserDiagnostics.NULL,
        )
    )
    assert s.current_state == state.READY
