  function checkIfYes() {
      if (document.getElementById('search_query').value == 'select_accession') {
        document.getElementById('search_accession').style.display = '';

        document.getElementById('search_gene').disabled = true;
        document.getElementById('search_gene').style.display = 'none';

        document.getElementById('search_desc').disabled = true;
        document.getElementById('search_desc').style.display = 'none';
      }
      else if (document.getElementById('search_query').value == 'select_gene') {
        document.getElementById('search_gene').style.display = '';

        document.getElementById('search_accession').disabled = true;
        document.getElementById('search_accession').style.display = 'none';

        document.getElementById('search_desc').disabled = true;
        document.getElementById('search_desc').style.display = 'none';

      }

      else if (document.getElementById('search_query').value == 'select_desc') {
        document.getElementById('search_desc').style.display = '';

        document.getElementById('search_accession').disabled = true;
        document.getElementById('search_accession').style.display = 'none';

        document.getElementById('search_gene').disabled = true;
        document.getElementById('search_gene').style.display = 'none';
      }


      else {
        document.getElementById('search_accession').style.display = 'none';
        document.getElementById('search_gene').style.display = 'none';
        document.getElementById('search_desc').style.display = 'none';
        }
      }