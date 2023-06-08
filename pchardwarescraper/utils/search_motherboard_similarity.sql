CREATE OR REPLACE FUNCTION search_motherboard_similarity(p_brand text, p_model_name text)
  RETURNS TABLE (full_name text) AS
$$
BEGIN
  RETURN QUERY
    SELECT m.full_name
    FROM motherboards AS m
    WHERE m.brand ILIKE p_brand AND similarity(m.full_name, p_model_name) > 0.4
    ORDER BY similarity(m.full_name, p_model_name) DESC
    LIMIT 1;
END;
$$
LANGUAGE plpgsql;
