from LAB1 import GLA

generatorIn = open("./Tests/simplePpjLang.lan", "r").read()
lexIn = open("./Tests/simplePpjLang.in", "r").read()

gen = GLA.Generator(generatorIn)
# gen.toString()
la = GLA.LA.LA(gen)

la.analyze(lexIn)
