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


class RawReviewAmazonReview2023Config(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        super(RawReviewAmazonReview2023Config, self).__init__(**kwargs)

        self.suffix = 'jsonl'
        self.domain = self.name[len(f'raw_review_'):]
        self.description = f'This is a subset for reviews in domain: {self.domain}.'
        self.data_dir = f'raw/review_categories/{self.domain}.jsonl'


class BenchmarkRatingOnlyAmazonReview2023Config(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        super(BenchmarkRatingOnlyAmazonReview2023Config, self).__init__(**kwargs)

        self.suffix = 'csv'
        self.kcore = self.name[:len('0core')]
        self.domain = self.name[len(f'0core_rating_only_'):]
        self.description = \
            f'This is the preprocessed benchmark in domain: {self.domain}.' \
            f'The preprocessing includes {self.kcore} filtering and <user, item> interaction deduplication'
        self.data_dir = f'benchmark/{self.kcore}/rating_only/{self.domain}.csv'


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
        # Raw review
        RawReviewAmazonReview2023Config(name='raw_review_All_Beauty'),
        RawReviewAmazonReview2023Config(name='raw_review_Toys_and_Games'),
        RawReviewAmazonReview2023Config(name='raw_review_Cell_Phones_and_Accessories'),
        RawReviewAmazonReview2023Config(name='raw_review_Industrial_and_Scientific'),
        RawReviewAmazonReview2023Config(name='raw_review_Gift_Cards'),
        RawReviewAmazonReview2023Config(name='raw_review_Musical_Instruments'),
        RawReviewAmazonReview2023Config(name='raw_review_Electronics'),
        RawReviewAmazonReview2023Config(name='raw_review_Handmade_Products'),
        RawReviewAmazonReview2023Config(name='raw_review_Arts_Crafts_and_Sewing'),
        RawReviewAmazonReview2023Config(name='raw_review_Baby_Products'),
        RawReviewAmazonReview2023Config(name='raw_review_Health_and_Household'),
        RawReviewAmazonReview2023Config(name='raw_review_Office_Products'),
        RawReviewAmazonReview2023Config(name='raw_review_Digital_Music'),
        RawReviewAmazonReview2023Config(name='raw_review_Grocery_and_Gourmet_Food'),
        RawReviewAmazonReview2023Config(name='raw_review_Sports_and_Outdoors'),
        RawReviewAmazonReview2023Config(name='raw_review_Home_and_Kitchen'),
        RawReviewAmazonReview2023Config(name='raw_review_Subscription_Boxes'),
        RawReviewAmazonReview2023Config(name='raw_review_Tools_and_Home_Improvement'),
        RawReviewAmazonReview2023Config(name='raw_review_Pet_Supplies'),
        RawReviewAmazonReview2023Config(name='raw_review_Video_Games'),
        RawReviewAmazonReview2023Config(name='raw_review_Kindle_Store'),
        RawReviewAmazonReview2023Config(name='raw_review_Clothing_Shoes_and_Jewelry'),
        RawReviewAmazonReview2023Config(name='raw_review_Patio_Lawn_and_Garden'),
        RawReviewAmazonReview2023Config(name='raw_review_Unknown'),
        RawReviewAmazonReview2023Config(name='raw_review_Books'),
        RawReviewAmazonReview2023Config(name='raw_review_Automotive'),
        RawReviewAmazonReview2023Config(name='raw_review_CDs_and_Vinyl'),
        RawReviewAmazonReview2023Config(name='raw_review_Beauty_and_Personal_Care'),
        RawReviewAmazonReview2023Config(name='raw_review_Amazon_Fashion'),
        RawReviewAmazonReview2023Config(name='raw_review_Magazine_Subscriptions'),
        RawReviewAmazonReview2023Config(name='raw_review_Software'),
        RawReviewAmazonReview2023Config(name='raw_review_Health_and_Personal_Care'),
        RawReviewAmazonReview2023Config(name='raw_review_Appliances'),
        RawReviewAmazonReview2023Config(name='raw_review_Movies_and_TV'),
        # Rating only - 0core
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_All_Beauty'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Toys_and_Games'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Cell_Phones_and_Accessories'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Industrial_and_Scientific'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Gift_Cards'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Musical_Instruments'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Electronics'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Handmade_Products'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Arts_Crafts_and_Sewing'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Baby_Products'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Health_and_Household'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Office_Products'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Digital_Music'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Grocery_and_Gourmet_Food'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Sports_and_Outdoors'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Home_and_Kitchen'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Subscription_Boxes'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Tools_and_Home_Improvement'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Pet_Supplies'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Video_Games'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Kindle_Store'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Clothing_Shoes_and_Jewelry'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Patio_Lawn_and_Garden'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Unknown'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Books'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Automotive'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_CDs_and_Vinyl'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Beauty_and_Personal_Care'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Amazon_Fashion'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Magazine_Subscriptions'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Software'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Health_and_Personal_Care'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Appliances'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='0core_rating_only_Movies_and_TV'),
        # Rating only - 5core
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_All_Beauty'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Toys_and_Games'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Cell_Phones_and_Accessories'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Industrial_and_Scientific'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Gift_Cards'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Musical_Instruments'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Electronics'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Arts_Crafts_and_Sewing'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Baby_Products'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Health_and_Household'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Office_Products'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Grocery_and_Gourmet_Food'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Sports_and_Outdoors'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Home_and_Kitchen'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Tools_and_Home_Improvement'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Pet_Supplies'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Video_Games'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Kindle_Store'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Clothing_Shoes_and_Jewelry'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Patio_Lawn_and_Garden'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Unknown'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Books'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Automotive'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_CDs_and_Vinyl'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Beauty_and_Personal_Care'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Magazine_Subscriptions'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Software'),
        BenchmarkRatingOnlyAmazonReview2023Config(name='5core_rating_only_Movies_and_TV'),
    ]

    def _info(self):
        features = None
        if isinstance(self.config, RawMetaAmazonReview2023Config):
            features = datasets.Features({
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
                'bought_together': datasets.Value('string'),    # TODO: Check this type
                'subtitle': datasets.Value('string'),
                'author': datasets.Value('string')
            })
        elif isinstance(self.config, RawReviewAmazonReview2023Config):
            # TODO: Check review features
            pass

        return datasets.DatasetInfo(
            description=_AMAZON_REVIEW_2023_DESCRIPTION + self.config.description,
            features=features
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
            if self.config.suffix == 'csv':
                colnames = file.readline().strip().split(',')
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
                elif self.config.suffix == 'csv':
                    line = line.strip().split(',')
                    dp = {k: v for k, v in zip(colnames, line)}
                else:
                    raise ValueError(f'Unknown suffix {self.config.suffix}.')
                yield idx, dp
