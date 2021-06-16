$(document).ready(() => {
	$("#searchForm").on('input', (e) => {
		let searchText = $('#searchBox').val();
		getMovies(searchText);
	});
});

function getMovies(searchText)
{
	axios.get('https://www.omdbapi.com?s='+searchText+"&apiKey=dd931d42")
		.then((response) => {
			console.log(response);
			let movies = response.data.Search;
			let output = '';
			$.each(movies, (index, movie) => {
				output += `
					<div class="card border-dark mb-3" style="max-width: 20rem;margin-left: auto;margin-right:auto;">
					<div class="card-header">${movie.Title} - ${movie.Year}</div>
					<div class="card-body text-dark" style="margin-left:auto;margin-right:auto;">
						<img src="${movie.Poster}"/><br>
						<a href="/addmovie/${movie.imdbID}" class="btn btn-success">Add</a>
					</div>
					</div>
				`;
			});
			console.log(output);
			$('#movies').html(output);
		})
		.catch((err) => {
			console.log(err);
		});
}