CREATE OR REPLACE FUNCTION search_processor_similarity(p_brand text, p_model_name text)
  RETURNS TABLE (full_name text) AS
$$
BEGIN
  RETURN QUERY
    SELECT p.full_name
    FROM processors AS p
    WHERE p.brand ILIKE p_brand AND similarity(p.full_name, p_model_name) > 0.4
    ORDER BY similarity(p.full_name, p_model_name) DESC
    LIMIT 1;
END;
$$
LANGUAGE plpgsql;
