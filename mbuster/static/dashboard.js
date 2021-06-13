$(document).ready(() => {
	$("#searchForm").on('input', (e) => {
		let searchText = $('#searchBox').val();
		getMovies(searchText);
	});
});

function getMovies(searchText)
{
	axios.get('http://www.omdbapi.com?s='+searchText+"&apiKey=dd931d42")
		.then((response) => {
			console.log(response);
			let movies = response.data.Search;
			let output = '';
			$.each(movies, (index, movie) => {
				output += `<form action="/addmovie/${movie.imdbID}" method="POST">
					<div class="card card-body mb-1">
					<div class="well text-center">
					<img src="${movie.Poster}"/>
					<h4>${movie.Title} - ${movie.Year}</h4>
					<input id=${movie.imdbID} type="submit" value="Add" class="btn btn-success"/>
					</div>
					</div>
					</form>
				`;
			});
			console.log(output);
			$('#movies').html(output);
		})
		.catch((err) => {
			console.log(err);
		});
}