'use strict';



cts.search(cts.andQuery([

            cts.jsonPropertyWordQuery('META_previous_curations','Keep'),

cts.jsonPropertyWordQuery('META_previous_curations','INSERT_USER_GROUP'),

cts.jsonPropertyRangeQuery('publication_date', '>=', xs.dateTime('REPLACE_FROM_DATET||REPLACE_FROM_HOUR00:00:00Z')),
cts.jsonPropertyRangeQuery('publication_date', '>=', xs.dateTime('REPLACE_FROM_DATET||REPLACE_FROM_HOUR00:00:00Z')),
            cts.collectionQuery("nifi_oss")]))


