import pageRank
import pageRank_baseline
import pytest

@pytest.mark.parametrize('dataset', ["airplaneRoutes", "stateborders", "redditHyperlinks"])
def test_equals_baseline(dataset):
	filename = f".\\data\\{dataset}.csv"
	results_opt = pageRank.run(filename, True, 10)
	results_baseline = pageRank_baseline.run(filename, True)
	for i in range(len(results_baseline)):
		# labels can be different (appear in different order) if two nodes have identical rank due to being functionally identical (e.g. having no inward links)
		assert results_baseline[i][1] == pytest.approx(results_opt[i][1]) # approx accounts for SLIGHT implementation-based differences