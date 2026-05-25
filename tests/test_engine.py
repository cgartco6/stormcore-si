from core.runtime.engine import StormCoreEngine


def test_engine_boot():
    engine = StormCoreEngine()
    engine.boot()

    assert engine is not None
