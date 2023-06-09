CREATE OR REPLACE FUNCTION search_video_card_similarity(v_brand text, v_model_name text)
  RETURNS TABLE (full_name text) AS
$$
BEGIN
  RETURN QUERY
    SELECT v.full_name
    FROM video_card AS v
    WHERE v.brand ILIKE v_brand AND similarity(v.full_name, v_model_name) > 0.1
    ORDER BY similarity(v.full_name, v_model_name) DESC
    LIMIT 1;
END;
$$
LANGUAGE plpgsql;
