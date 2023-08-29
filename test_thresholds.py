from syncDco.main import main
from syncDco import auto
import pytest

@pytest.fixture("DCOFrequencyCapProspectingFunnelLevel2")
def test_performance_thresholds():
    freBx = (main("DCOFrequencyCapProspectingFunnelLevel2", "frequency").ValidateResposeData(
        "DCOFrequencyCapProspectingFunnelLevel2"))
    assert freBx == True