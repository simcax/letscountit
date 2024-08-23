CREATE MIGRATION m1g7jx5zmnbxvwyoaf6dggmlxkd7idj5imo3emuza75jcp2vr7jaoq
    ONTO initial
{
  CREATE TYPE default::counter {
      CREATE PROPERTY uuid: std::uuid;
  };
};
