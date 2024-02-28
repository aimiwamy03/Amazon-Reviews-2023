import json

import datasets


_AMAZON_REVIEW_2023_DESCRIPTION = """\
Amazon Review 2023 is an updated version of the Amazon Review 2018 dataset.
This dataset mainly includes reviews (ratings, text) and item metadata (desc-
riptions, category information, price, brand, and images). Compared to the pre-
vious versions, the 2023 version features larger size, newer reviews (up to Sep
2023), richer and cleaner meta data, and finer-grained timestamps (from day to 
milli-second).

"""


class RawMetaAmazonReview2023Config(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        super(RawMetaAmazonReview2023Config, self).__init__(**kwargs)

        self.suffix = 'jsonl'
        self.domain = self.name[len(f'raw_meta_'):]
        self.description = f'This is a subset for items in domain: {self.domain}.'
        self.data_dir = f'raw/meta_categories/meta_{self.domain}.jsonl'


class AmazonReview2023(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        RawMetaAmazonReview2023Config(
            name='raw_meta_All_Beauty'
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_AMAZON_REVIEW_2023_DESCRIPTION + self.config.description
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(self.config.data_dir)
        return [
            datasets.SplitGenerator(
                name='full',
                gen_kwargs={"filepath": dl_dir}
            )
        ]

    def _generate_examples(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            for idx, line in enumerate(file):
                if self.config.suffix == 'jsonl':
                    try:
                        dp = json.loads(line)
                        """
                        For item metadata, 'details' is free-form structured data
                        Here we dump it to string to make huggingface datasets easy
                        to store.
                        """
                        if isinstance(self.config, RawMetaAmazonReview2023Config) and \
                           'details' in dp:
                            dp['details'] = json.dumps(dp['details'])
                    except:
                        continue
                else:
                    raise ValueError(f'Unknown suffix {self.config.suffix}.')
                yield idx, dp
