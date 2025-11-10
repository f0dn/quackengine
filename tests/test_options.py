from engine import Engine

def test_options(capsys):
    engine = Engine()
    engine.add_options("Hash", "spin", {"default": 1, "min": 1, "max": 128})
    captured = capsys.readouterr()
    assert captured.out == "option name Hash type spin default 1 min 1 max 128\n"
    assert engine.options_dict == {"Hash": {"type": "spin", "value": {"default": 1, "min": 1, "max": 128}}}
    engine.add_options("NalimovPath", "string", {"default": "<empty>"})
    cap1 = capsys.readouterr()
    assert cap1.out == "option name NalimovPath type string default <empty>\n"
    assert engine.options_dict == {"Hash": {"type": "spin", "value": {"default": 1, "min": 1, "max": 128}}, "NalimovPath": {"type": "string", "value": {"default": "<empty>"}}}
    engine.add_options("NalimovCache", "spin", {"default": 1, "min": 1, "max": 32})
    cap2 = capsys.readouterr()
    assert cap2.out == "option name NalimovCache type spin default 1 min 1 max 32\n"
    engine.add_options("Nullmove", "check", {"default": "true"})
    cap3 = capsys.readouterr()
    assert cap3.out == "option name Nullmove type check default true\n"
    engine.add_options("Style", "combo", {"default": "Normal", "var": ["Solid", "Normal", "Risky"]})
    cap4 = capsys.readouterr()
    assert cap4.out == "option name Style type combo default Normal var Solid var Normal var Risky\n"