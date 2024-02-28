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
        # Raw item metadata
        RawMetaAmazonReview2023Config(name='raw_meta_All_Beauty'),
        RawMetaAmazonReview2023Config(name='raw_meta_Toys_and_Games'),
        RawMetaAmazonReview2023Config(name='raw_meta_Cell_Phones_and_Accessories'),
        RawMetaAmazonReview2023Config(name='raw_meta_Industrial_and_Scientific'),
        RawMetaAmazonReview2023Config(name='raw_meta_Gift_Cards'),
        RawMetaAmazonReview2023Config(name='raw_meta_Musical_Instruments'),
        RawMetaAmazonReview2023Config(name='raw_meta_Electronics'),
        RawMetaAmazonReview2023Config(name='raw_meta_Handmade_Products'),
        RawMetaAmazonReview2023Config(name='raw_meta_Arts_Crafts_and_Sewing'),
        RawMetaAmazonReview2023Config(name='raw_meta_Baby_Products'),
        RawMetaAmazonReview2023Config(name='raw_meta_Health_and_Household'),
        RawMetaAmazonReview2023Config(name='raw_meta_Office_Products'),
        RawMetaAmazonReview2023Config(name='raw_meta_Digital_Music'),
        RawMetaAmazonReview2023Config(name='raw_meta_Grocery_and_Gourmet_Food'),
        RawMetaAmazonReview2023Config(name='raw_meta_Sports_and_Outdoors'),
        RawMetaAmazonReview2023Config(name='raw_meta_Home_and_Kitchen'),
        RawMetaAmazonReview2023Config(name='raw_meta_Subscription_Boxes'),
        RawMetaAmazonReview2023Config(name='raw_meta_Tools_and_Home_Improvement'),
        RawMetaAmazonReview2023Config(name='raw_meta_Pet_Supplies'),
        RawMetaAmazonReview2023Config(name='raw_meta_Video_Games'),
        RawMetaAmazonReview2023Config(name='raw_meta_Kindle_Store'),
        RawMetaAmazonReview2023Config(name='raw_meta_Clothing_Shoes_and_Jewelry'),
        RawMetaAmazonReview2023Config(name='raw_meta_Patio_Lawn_and_Garden'),
        RawMetaAmazonReview2023Config(name='raw_meta_Unknown'),
        RawMetaAmazonReview2023Config(name='raw_meta_Books'),
        RawMetaAmazonReview2023Config(name='raw_meta_Automotive'),
        RawMetaAmazonReview2023Config(name='raw_meta_CDs_and_Vinyl'),
        RawMetaAmazonReview2023Config(name='raw_meta_Beauty_and_Personal_Care'),
        RawMetaAmazonReview2023Config(name='raw_meta_Amazon_Fashion'),
        RawMetaAmazonReview2023Config(name='raw_meta_Magazine_Subscriptions'),
        RawMetaAmazonReview2023Config(name='raw_meta_Software'),
        RawMetaAmazonReview2023Config(name='raw_meta_Health_and_Personal_Care'),
        RawMetaAmazonReview2023Config(name='raw_meta_Appliances'),
        RawMetaAmazonReview2023Config(name='raw_meta_Movies_and_TV'),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_AMAZON_REVIEW_2023_DESCRIPTION + self.config.description,
            features=datasets.Features({
                'main_category': datasets.Value('string'),
                'title': datasets.Value('string'),
                'average_rating': datasets.Value(dtype='float64'),
                'rating_number': datasets.Value(dtype='int64'),
                'features': datasets.Sequence(datasets.Value('string')),
                'description': datasets.Sequence(datasets.Value('string')),
                'price': datasets.Value('string'),
                'images': datasets.Sequence({
                    'hi_res': datasets.Value('string'),
                    'large': datasets.Value('string'),
                    'thumb': datasets.Value('string'),
                    'variant': datasets.Value('string')
                }),
                'videos': datasets.Sequence({
                    'title': datasets.Value('string'),
                    'url': datasets.Value('string'),
                    'user_id': datasets.Value('string')
                }),
                'store': datasets.Value('string'),
                'categories': datasets.Sequence(datasets.Value('string')),
                'details': datasets.Value('string'),
                'parent_asin': datasets.Value('string'),
                'bought_together': datasets.Value(dtype='null', id=None),
                'subtitle': datasets.Value('string'),
                'author': datasets.Value('string')
            })
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
                        if isinstance(self.config, RawMetaAmazonReview2023Config):
                            if 'details' in dp:
                                dp['details'] = json.dumps(dp['details'])
                            if 'price' in dp:
                                dp['price'] = str(dp['price'])
                            for optional_key in ['subtitle', 'author']:
                                if optional_key not in dp:
                                    dp[optional_key] = None
                            for i in range(len(dp['images'])):
                                for k in ['hi_res', 'large', 'thumb', 'variant']:
                                    if k not in dp['images'][i]:
                                        dp['images'][i][k] = None
                            for i in range(len(dp['videos'])):
                                for k in ['title', 'url', 'user_id']:
                                    if k not in dp['videos'][i]:
                                        dp['videos'][i][k] = None
                    except:
                        continue
                else:
                    raise ValueError(f'Unknown suffix {self.config.suffix}.')
                yield idx, dp
