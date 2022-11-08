console.log("inside retrieve doc titles")
'use strict';
cts.search(cts.andQuery([

            cts.jsonPropertyWordQuery('META_previous_curations','Keep'),

cts.jsonPropertyWordQuery('META_previous_curations','INSERT_USER_GROUP'),

cts.jsonPropertyRangeQuery('publication_date', '>=', xs.dateTime('REPLACE_FROM_DATE')),
cts.jsonPropertyRangeQuery('publication_date', '>=', xs.dateTime('REPLACE_TO_DATE')),
        // cts.jsonPropertyRangeQuery('publication_date', '<=', xs.dateTime('2022-08-16T23:59:59Z')),
        // cts.jsonPropertyRangeQuery('publication_date', '>=', xs.dateTime('2022-08-01T00:00:00Z')),
            cts.collectionQuery("nifi_oss")]))


