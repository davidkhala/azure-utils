from pathlib import Path
from typing import Any

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentAnalysisFeature, AnalyzeResult


class Recognizer:
    def __init__(self, endpoint, credential):
        self.client = DocumentIntelligenceClient(endpoint=endpoint, credential=credential)

    def extract_entities(self, file: Path, focus: list[str] = None)->list[dict]:
        options:dict[str, Any] = {
            'model_id': "prebuilt-layout",
            'features': [DocumentAnalysisFeature.KEY_VALUE_PAIRS],
        }
        if focus:
            options['features'].append(DocumentAnalysisFeature.QUERY_FIELDS)
            options['query_fields'] = focus

        r = self.process(file, **options)
        if focus:
            return [
                {_: v.content for _, v in doc.fields.items()}
                for doc in r.documents
            ]

        return [
            {pair['key']['content']: pair['value']['content'] if pair.get('value') else None}
            for pair in r.key_value_pairs
        ]

    @staticmethod
    def dict_of(result: AnalyzeResult):
        d = result.as_dict()
        del d['apiVersion']
        del d['modelId']
        del d['stringIndexType']
        return d

    def process(self, file: Path, **kwargs) -> AnalyzeResult:
        with open(file, "rb") as f:
            content = f.read()
        promise = self.client.begin_analyze_document(
            body=AnalyzeDocumentRequest(bytes_source=content),
            **kwargs
        )
        return promise.result()
