import sys, pathlib, io
from urllib.parse import unquote
import aaf2

def get_all_source_paths(aaf:aaf2.content.ContentStorage) -> dict[aaf2.mobs.Mob, str]:

	results = dict()

	for mob in [m for m in aaf.mobs if isinstance(m, aaf2.mobs.SourceMob)]:

		descriptor = mob.descriptor
		if isinstance(descriptor, aaf2.essence.PCMDescriptor):

			# Look for NetworkLocator
			for loc in [l for l in descriptor.locator if l.name in ("NetworkLocator",)]:
				for prop_url in [u for u in loc.properties() if u.name in ("URLString",)]:
					results[mob] = str(unquote(prop_url.value))
	
	return results

def essence_exists(filename:str, paths_search:list[str]):

	for path_search in paths_search:
		print(pathlib.Path(path_search, filename))
		if pathlib.Path(path_search, filename).is_file():
			return True
		
	return False

def write_path_report(report:dict[aaf2.mobs.Mob, str], file_report:io.TextIOWrapper, paths_search:list[str]):

	for mob, path in report.items():
		print(f"{mob.name if mob.name else mob}\t{pathlib.Path(path).name}\t{essence_exists(pathlib.Path(path).name, paths_search)}", file=file_report)



def main(path_aaf:str, path_dest:str, paths_search:list[str]):
	"""Given an AAF, gather the media at `path_dest`"""

	with aaf2.open(path_aaf) as file_aaf:

		print(f"Reading {path_aaf}...")

		timelines = list(file_aaf.content.toplevel())
		print(f"{len(timelines)} Timeline(s):")
		for tl in timelines:
			print(f" - {tl.name}")
		
		source_mob_paths = get_all_source_paths(file_aaf.content)
	
		with open(path_dest, "w") as file_report:
			write_path_report(report=source_mob_paths, file_report=file_report, paths_search=paths_search)

	print(len(source_mob_paths), "source(s) written")
"""
		print("")
		print("Morbs:")
			#print(mob,":")
			descr = mob.descriptor
			if isinstance(descr, aaf2.essence.PCMDescriptor):
				for loc_net in [l for l in descr.locator if l.name=="NetworkLocator"]:
					for prop_url in [u for u in loc_net.properties() if u.name=="URLString"]:
						print(str(mob.name), "    |   ", prop_url.name," :: ", prop_url.value)
			else:
				print(str(mob.name), "     |     ****SKIP")
"""	



if __name__ == "__main__":
	
	if not len(sys.argv) > 2:
		sys.exit(f"Usage: {__file__} input.aaf dest_folder [additional_search_folder ...]")
	
	main(path_aaf=sys.argv[1], path_dest=sys.argv[2], paths_search=sys.argv[3:])