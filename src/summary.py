from pandas import DataFrame
from ollama import generate


class AISummary:

    def __init__(self,model:str, avgPace: DataFrame, consistency: DataFrame, tyreStategy: DataFrame, winnerComparison: DataFrame, allDrivers: DataFrame) -> None:

        self.avgPace: DataFrame = avgPace
        self.consistency: DataFrame = consistency
        self.tyreStrategy: DataFrame = tyreStategy
        self.winnerComparison: DataFrame = winnerComparison
        self.allDrivers: DataFrame = allDrivers


        self._prompt: str = None
        self._outputFile:str = "output/summary.md"
        self._model: str = model

    def generatePrompt(self) -> None:
        prompt: str = f"""
        Erkläre die wichtigsten Renntrends und Strategien dieses Formel-1-Rennens
        basierend auf den folgenden Daten.

        Durchschnittliche Rundenzeiten:
        {self.avgPace.to_string(index=False)}

        Konstanz der Fahrer (Standardabweichung der Rundenzeit):
        {self.consistency.to_string(index=False)}

        Reifenwechsel:
        {self.tyreStrategy.to_string(index=False)}

        Vergleich zum Gewinner:
        {self.winnerComparison.to_string(index=False)}

        Liste aller Fahrer und ihre Namen, Nummern, Team etc.:
        {self.allDrivers.to_string(index=False)}

        Zielgruppe sind technisch interessierte Leser. Formatiere deine Antwort als Markdown-Dokument. Ziehe aus den Daten auch verschiedene Schlüsse. Versetzte dich in die Lage eines Formel-1 Renningenieur. Gebe nicht alles genau so wieder wie es auch in den Daten steht, sondern für Menschen einfach lesbar.
        """

        self.prompt = prompt
        return 0

    def summarizeStrategy(self) -> str:
        if self.prompt == None: raise("No Prompt Error")

        response = generate(model=self._model, prompt=self.prompt)
        with open(self._outputFile, "w", encoding="utf-8") as f:
            f.write(response.response)

        print(f"Summary written to {self._outputFile}")
        return response.response