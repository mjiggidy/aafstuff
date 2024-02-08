import sys, pathlib
import aaf2

def main(path_aaf:str, path_dest:str, paths_search:list[str]):
	"""Given an AAF, gather the media at `path_dest`"""

	with aaf2.open(path_aaf) as file_aaf:

		print(f"Reading {path_aaf}...")

		timelines = list(file_aaf.content.toplevel())
		print(f"{len(timelines)} Timeline(s):")
		for tl in timelines:
			print(f" - {tl.name}")

		print("")
		print("Morbs:")
		for mob in [m for m in file_aaf.content.mobs if isinstance(m, aaf2.mobs.SourceMob)]:
			print(mob,":")
			descr = mob.descriptor
			if isinstance(descr, aaf2.essence.PCMDescriptor):
				for loc_net in [l for l in descr.locator if l.name=="NetworkLocator"]:
					for prop_url in [u for u in loc_net.properties() if u.name=="URLString"]:
						print(prop_url.name," :: ", prop_url.value)
			else:
				print("****SKIP")
		



if __name__ == "__main__":
	
	if not len(sys.argv) > 2:
		sys.exit(f"Usage: {__file__} input.aaf dest_folder [additional_search_folder ...]")
	
	main(path_aaf=sys.argv[1], path_dest=sys.argv[2], paths_search=sys.argv[3:])