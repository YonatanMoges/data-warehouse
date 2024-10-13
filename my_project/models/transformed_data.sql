-- models/example/transformed_data.sql

WITH base AS (
    SELECT *
    FROM {{ ref('cleaned_data') }}
),
transformed AS (
    -- Apply transformations, e.g., renaming columns, filtering, and formatting
    SELECT
        "Channel Title" AS channel_title,
        "Channel Username" AS channel_username,
        "ID" AS message_id,
        "Message" AS message,
        "Date" AS message_date,
        "Media Path" AS media_path
    FROM base
    WHERE "Message" IS NOT NULL  -- Remove rows with missing messages
)

SELECT * FROM transformed
